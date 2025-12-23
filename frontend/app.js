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
