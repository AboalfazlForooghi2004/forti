function loadData() {
    fetch("/api/phase1/addresses")
        .then(res => res.json())
        .then(data => {
            document.getElementById("addresses").textContent =
                JSON.stringify(data.address_objects, null, 2);

            document.getElementById("groups").textContent =
                JSON.stringify(data.address_groups, null, 2);
        })
        .catch(err => alert("خطا در دریافت اطلاعات"));
}
function loadDuplicates() {
  fetch("/api/phase2/duplicates")
    .then(r => r.json())
    .then(data => {
      document.getElementById("duplicates").textContent =
        JSON.stringify(data.duplicates, null, 2);
    });
}

function findGroups() {
  const ip = document.getElementById("ipInput").value;

  fetch("/api/phase2/ip-groups", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ip })
  })
    .then(r => r.json())
    .then(data => {
      document.getElementById("groupsResult").textContent =
        JSON.stringify(data.groups, null, 2);
    });
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

  fetch("/api/phase3/vip", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(d => phase3Result.textContent = JSON.stringify(d, null, 2));
}

function updatePolicy() {
  fetch("/api/phase3/policy", {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      policy_id: policyId.value,
      vip_name: policyVip.value
    })
  })
  .then(r => r.json())
  .then(d => phase3Result.textContent = JSON.stringify(d, null, 2));
}
function runAutomation() {
  const targets = p4Targets.value.split("\n").map(line => {
    const [ip, port] = line.split(":");
    return { ip, port: parseInt(port) };
  });

  fetch("/api/phase4/publish", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      external_ip: p4ExtIp.value,
      interface: p4Intf.value,
      policy_id: parseInt(p4Policy.value),
      targets
    })
  })
  .then(r => r.json())
  .then(d => p4Result.textContent = JSON.stringify(d, null, 2))
  .catch(() => alert("Automation failed"));
}
function rollbackVIP() {
  fetch("/api/phase5/rollback", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ vip_name: rbVip.value })
  })
  .then(r => r.json())
  .then(d => rbResult.textContent = JSON.stringify(d, null, 2))
  .catch(() => alert("Rollback failed"));
}
