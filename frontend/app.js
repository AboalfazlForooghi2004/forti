// Utility function for error handling
function handleError(error, elementId) {
    console.error('Error:', error);
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = `❌ خطا: ${error.message || 'عملیات ناموفق بود'}`;
        el.style.color = '#ef4444';
    }
}

// Utility function for success display
function displayResult(data, elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = JSON.stringify(data, null, 2);
        el.style.color = '#e5e7eb';
    }
}

function loadData() {
    const addressesEl = document.getElementById("addresses");
    const groupsEl = document.getElementById("groups");
    
    addressesEl.textContent = "در حال دریافت...";
    groupsEl.textContent = "در حال دریافت...";

    fetch("/api/phase1/addresses")
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            displayResult(data.address_objects, "addresses");
            displayResult(data.address_groups, "groups");
        })
        .catch(err => {
            handleError(err, "addresses");
            handleError(err, "groups");
        });
}

function loadDuplicates() {
    const el = document.getElementById("duplicates");
    el.textContent = "در حال بررسی...";

    fetch("/api/phase2/duplicates")
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(data => displayResult(data, "duplicates"))
        .catch(err => handleError(err, "duplicates"));
}

function findGroups() {
    const ip = document.getElementById("ipInput").value;
    const resultEl = document.getElementById("groupsResult");

    if (!ip) {
        resultEl.textContent = "⚠️ لطفاً IP را وارد کنید";
        return;
    }

    resultEl.textContent = "در حال جستجو...";

    fetch("/api/phase2/ip-groups", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip })
    })
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(data => displayResult(data, "groupsResult"))
        .catch(err => handleError(err, "groupsResult"));
}

function createVIP() {
    const payload = {
        name: vipName.value,
        external_ip: extIp.value,
        mapped_ip: mapIp.value,
        interface: vipIntf.value,
        external_port: extPort.value,
        mapped_port: mapPort.value
    };

    // Validation
    if (!payload.name || !payload.external_ip || !payload.mapped_ip) {
        phase3Result.textContent = "⚠️ فیلدهای ضروری را پر کنید";
        return;
    }

    phase3Result.textContent = "در حال ایجاد VIP...";

    fetch("/api/phase3/vip", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    })
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(d => displayResult(d, "phase3Result"))
        .catch(err => handleError(err, "phase3Result"));
}

function updatePolicy() {
    const payload = {
        policy_id: policyId.value,
        vip_name: policyVip.value
    };

    if (!payload.policy_id || !payload.vip_name) {
        phase3Result.textContent = "⚠️ Policy ID و VIP Name ضروری است";
        return;
    }

    phase3Result.textContent = "در حال به‌روزرسانی...";

    fetch("/api/phase3/policy", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    })
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(d => displayResult(d, "phase3Result"))
        .catch(err => handleError(err, "phase3Result"));
}

function runAutomation() {
    const targetsText = p4Targets.value.trim();
    
    if (!targetsText) {
        p4Result.textContent = "⚠️ لطفاً targets را وارد کنید";
        return;
    }

    const targets = targetsText.split("\n")
        .filter(line => line.trim())
        .map(line => {
            const [ip, port] = line.split(":");
            return { ip: ip.trim(), port: parseInt(port) };
        });

    const payload = {
        external_ip: p4ExtIp.value,
        interface: p4Intf.value,
        policy_id: parseInt(p4Policy.value),
        targets
    };

    p4Result.textContent = "در حال اجرای automation...";

    fetch("/api/phase4/publish", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    })
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(d => displayResult(d, "p4Result"))
        .catch(err => handleError(err, "p4Result"));
}

function rollbackVIP() {
    const vipName = rbVip.value.trim();
    
    if (!vipName) {
        rbResult.textContent = "⚠️ نام VIP را وارد کنید";
        return;
    }

    if (!confirm(`آیا مطمئن هستید که می‌خواهید VIP "${vipName}" را rollback کنید؟`)) {
        return;
    }

    rbResult.textContent = "در حال rollback...";

    fetch("/api/phase5/rollback", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ vip_name: vipName })
    })
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(d => displayResult(d, "rbResult"))
        .catch(err => handleError(err, "rbResult"));
}