// Tab switching. Everything else is server-rendered.
(function () {
  const tabs = document.querySelectorAll('[role="tab"]');

  function show(tab) {
    tabs.forEach(function (t) {
      const selected = t === tab;
      t.setAttribute("aria-selected", selected ? "true" : "false");
      document.getElementById(t.getAttribute("aria-controls")).hidden = !selected;
    });
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { show(tab); });
  });
})();
