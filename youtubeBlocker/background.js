chrome.webNavigation.onCompleted.addListener((details) => {
    if (details.url.includes("youtube.com")) {
        const now = Date.now();
        chrome.storage.local.get("blockStartTime", (data) => {
            const blockStartTime = data.blockStartTime || 0;
            const blockDuration = 10 * 60 * 1000; // 10 minutes

            if (now > blockStartTime + blockDuration) {
                chrome.storage.local.set({ blockStartTime: now });
            }
        });
    }
}, { url: [{ hostContains: "youtube.com" }] });
