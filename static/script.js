document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript code here
    // Ensure you're accessing elements only after the DOM is fully loaded
    document.querySelector('.navbar-toggler').addEventListener('click', function() {
        document.querySelector('.navbar ul').classList.toggle('show');
    });

    document.getElementById("branch").addEventListener("change", function() {
        var branch = this.value;
        var semesterSelect = document.getElementById("sem");
        semesterSelect.innerHTML = ""; // Clear previous options

        if (branch === "Branch1") {
            addOption(semesterSelect, "Semester1", "Semester1");
            addOption(semesterSelect, "Semester2", "Semester2");
            addOption(semesterSelect, "Semester3", "Semester3");
        } else if (branch === "Branch2") {
            addOption(semesterSelect, "Semester4", "Semester4");
            addOption(semesterSelect, "Semester5", "Semester5");
            addOption(semesterSelect, "Semester6", "Semester6");
        } else if (branch === "Branch3") {
            addOption(semesterSelect, "Semester7", "Semester7");
            addOption(semesterSelect, "Semester8", "Semester8");
        }
    });

    function addOption(selectElement, text, value) {
        var option = document.createElement("option");
        option.text = text;
        option.value = value;
        selectElement.add(option);
    }
});
