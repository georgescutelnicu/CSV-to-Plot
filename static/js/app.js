function showSettings() {
    var chartType = document.getElementById("chart-type").value;
    var settingsBar = document.getElementById("settings-bar");
    var settingsHist = document.getElementById("settings-hist");

    if (chartType === "bar") {
        settingsBar.style.display = "block";
        settingsHist.style.display = "none";
    } else if (chartType === "hist") {
        settingsBar.style.display = "none";
        settingsHist.style.display = "block";
    } else {
        // Handle other chart types if needed
        settingsBar.style.display = "none";
        settingsHist.style.display = "none";
    }
}