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
