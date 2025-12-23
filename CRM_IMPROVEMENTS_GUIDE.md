# CRM Improvements Implementation Guide

## Overview
This guide contains 4 improvements to the CRM:
1. Client creation flow - autopopulate contact info
2. Services - add "Special Projects" field
3. Service Banner - hourly rate selection
4. Prospects - remove $75k auto-populate

---

## Improvement 1: Client Creation Flow - Autopopulate Contact Info

### Problem
When creating a client, contact info doesn't flow into the next screen. Users have to re-enter it.

### Solution
Pass client contact info through the form flow using session storage or URL parameters.

### Files to Modify:
- `templates/client_form.html` or client creation template
- `main.py` - client creation route

### Implementation:

**In the client creation form template**, add hidden fields or use JavaScript to store form data:

```html
<!-- Add to client creation form -->
<script>
// Store form data when moving to next step
function saveFormData() {
    const formData = {
        name: document.getElementById('name')?.value || '',
        email: document.getElementById('email')?.value || '',
        phone: document.getElementById('phone')?.value || '',
        address: document.getElementById('address')?.value || '',
        city: document.getElementById('city')?.value || '',
        state: document.getElementById('state')?.value || '',
        zip: document.getElementById('zip')?.value || ''
    };
    sessionStorage.setItem('clientFormData', JSON.stringify(formData));
}

// Load form data when page loads
window.addEventListener('DOMContentLoaded', function() {
    const savedData = sessionStorage.getItem('clientFormData');
    if (savedData) {
        const data = JSON.parse(savedData);
        // Autopopulate fields
        if (document.getElementById('name')) document.getElementById('name').value = data.name || '';
        if (document.getElementById('email')) document.getElementById('email').value = data.email || '';
        if (document.getElementById('phone')) document.getElementById('phone').value = data.phone || '';
        if (document.getElementById('address')) document.getElementById('address').value = data.address || '';
        if (document.getElementById('city')) document.getElementById('city').value = data.city || '';
        if (document.getElementById('state')) document.getElementById('state').value = data.state || '';
        if (document.getElementById('zip')) document.getElementById('zip').value = data.zip || '';
    }
});
</script>
```

**In main.py**, modify the client creation route to pass data to next screen:

```python
@app.post("/clients/new")
async def create_client(request: Request):
    form = await request.form()
    # ... existing client creation code ...
    
    # After creating client, redirect with client_id so next screen can fetch contact info
    return RedirectResponse(url=f"/clients/{client.id}/contacts/new?client_id={client.id}", status_code=303)
```

---

## Improvement 2: Services - Add "Special Projects" Field

### Problem
Need to add a "Special Projects" field to services.

### Solution
Add `special_projects` field to Service model and forms.

### Files to Modify:
- `models.py` - Service model
- Service creation/editing templates
- `main.py` - service routes

### Implementation:

**In models.py**, add to Service model:

```python
class Service(Base):
    # ... existing fields ...
    special_projects = Column(String, nullable=True)  # Add this line
```

**In service form template**, add field:

```html
<div class="form-group">
    <label for="special_projects">Special Projects</label>
    <textarea id="special_projects" name="special_projects" class="form-control" rows="3">{{ service.special_projects if service else '' }}</textarea>
</div>
```

**In main.py**, update service creation/update routes:

```python
@app.post("/services/new")
async def create_service(request: Request):
    form = await request.form()
    # ... existing code ...
    special_projects = form.get("special_projects", "")
    # Add to service creation
    service = Service(
        # ... existing fields ...
        special_projects=special_projects
    )
```

---

## Improvement 3: Service Banner - Hourly Rate Selection

### Problem
Need to allow selecting "hourly" billing type and entering hourly rate.

### Solution
Add billing type selector and hourly rate input field.

### Files to Modify:
- Service model (add `billing_type` and `hourly_rate` fields)
- Service form templates
- `main.py` - service routes

### Implementation:

**In models.py**, add to Service model:

```python
class Service(Base):
    # ... existing fields ...
    billing_type = Column(String, default="fixed")  # "fixed" or "hourly"
    hourly_rate = Column(Numeric(10, 2), nullable=True)  # Add this
```

**In service form template**, add fields:

```html
<div class="form-group">
    <label for="billing_type">Billing Type</label>
    <select id="billing_type" name="billing_type" class="form-control" onchange="toggleHourlyRate()">
        <option value="fixed" {{ 'selected' if (not service or service.billing_type == 'fixed') else '' }}>Fixed Price</option>
        <option value="hourly" {{ 'selected' if (service and service.billing_type == 'hourly') else '' }}>Hourly</option>
    </select>
</div>

<div class="form-group" id="hourly_rate_group" style="display: none;">
    <label for="hourly_rate">Hourly Rate ($)</label>
    <input type="number" id="hourly_rate" name="hourly_rate" class="form-control" step="0.01" min="0" value="{{ service.hourly_rate if service and service.hourly_rate else '' }}">
</div>

<script>
function toggleHourlyRate() {
    const billingType = document.getElementById('billing_type').value;
    const hourlyRateGroup = document.getElementById('hourly_rate_group');
    if (billingType === 'hourly') {
        hourlyRateGroup.style.display = 'block';
        document.getElementById('hourly_rate').required = true;
    } else {
        hourlyRateGroup.style.display = 'none';
        document.getElementById('hourly_rate').required = false;
    }
}

// Run on page load
window.addEventListener('DOMContentLoaded', toggleHourlyRate);
</script>
```

**In main.py**, update service routes:

```python
@app.post("/services/new")
async def create_service(request: Request):
    form = await request.form()
    billing_type = form.get("billing_type", "fixed")
    hourly_rate = form.get("hourly_rate")
    
    service = Service(
        # ... existing fields ...
        billing_type=billing_type,
        hourly_rate=float(hourly_rate) if hourly_rate and billing_type == "hourly" else None
    )
```

---

## Improvement 4: Prospects - Remove $75k Auto-populate

### Problem
$75k auto-populates for all prospects even when revenue is not entered.

### Solution
Only show revenue if explicitly entered. Remove default value.

### Files to Modify:
- `main.py` - prospect creation/display routes
- Prospect templates

### Implementation:

**In main.py**, find prospect creation route and remove default:

```python
@app.post("/prospects/new")
async def create_prospect(request: Request):
    form = await request.form()
    estimated_revenue = form.get("estimated_revenue", "")
    
    # Only set revenue if explicitly provided
    estimated_revenue_value = None
    if estimated_revenue and estimated_revenue.strip():
        try:
            estimated_revenue_value = float(estimated_revenue)
        except ValueError:
            estimated_revenue_value = None
    
    prospect = Prospect(
        # ... existing fields ...
        estimated_revenue=estimated_revenue_value  # No default, only if provided
    )
```

**In prospect form template**, ensure no default value:

```html
<div class="form-group">
    <label for="estimated_revenue">Estimated Revenue ($)</label>
    <input type="number" id="estimated_revenue" name="estimated_revenue" class="form-control" step="0.01" min="0" value="{{ prospect.estimated_revenue if prospect and prospect.estimated_revenue else '' }}" placeholder="Enter revenue (optional)">
</div>
```

**In prospect list/display templates**, only show if value exists:

```html
{% if prospect.estimated_revenue %}
    <span>${{ "{:,.2f}".format(prospect.estimated_revenue) }}</span>
{% else %}
    <span class="text-muted">Not specified</span>
{% endif %}
```

---

## Testing Checklist

After implementing each improvement:

- [ ] **Improvement 1**: Create a client, verify contact info autopopulates in next screen
- [ ] **Improvement 2**: Create/edit a service, verify "Special Projects" field appears and saves
- [ ] **Improvement 3**: Create/edit a service, select "hourly", verify hourly rate field appears and saves
- [ ] **Improvement 4**: Create a prospect without revenue, verify no $75k appears

---

## Deployment Steps

1. Make changes to files locally
2. Test each improvement
3. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Implement CRM improvements: autopopulate, special projects, hourly rates, prospect revenue fix"
   git push
   ```
4. Render will auto-deploy (wait 3-5 minutes)
5. Test on live site

---

## Need Help?

If you need me to create the actual file modifications, let me know and I can create complete updated files for you to replace.

