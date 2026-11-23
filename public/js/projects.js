// CENTRAL PROJECT REGISTRY - edit this file to change a project's preview.
// status: "live" (set production to the real deployed address) | "local" (works only while the demo
//         runs on this computer, address in "local") | "in-progress" | "coming-soon".
// Previews only appear for "live", or for "local" while this site is opened from localhost / 127.0.0.1.
// Never type an address here until that website really exists.
window.PN = {
  projects: {
    "olive-and-oak": {
        "name": "Olive & Oak",
        "status": "live",
        "production": "/demos/olive-and-oak/",
        "local": ""
    },
    "the-cut": {
        "name": "THE CUT",
        "status": "live",
        "production": "/demos/the-cut/",
        "local": ""
    },
    "nexora-business-solutions": {
        "name": "Nexora Business Solutions",
        "status": "live",
        "production": "/demos/nexora/",
        "local": ""
    }
},
  url: function (slug) {
    var p = this.projects[slug];
    if (!p) return '';
    if (p.status === 'live') return p.production || '';
    if (p.status === 'local' && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) return p.local || '';
    return '';
  }
};
