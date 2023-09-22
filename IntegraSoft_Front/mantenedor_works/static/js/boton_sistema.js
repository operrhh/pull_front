
const select = document.getElementById("base_datos");     
const selectedValue = localStorage.getItem("selectedValue");
if (selectedValue) {
    select.value = selectedValue;
}

select.addEventListener("change", function () {
    localStorage.setItem("selectedValue", this.value);
});
