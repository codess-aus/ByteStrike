const MAX_RETRIES = 3;
const BASE_DELAY_MS = 1000;

async function retrieveAndDecodeBlueprint(url) {
    let lastError;
    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
        try {
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), 10000);
            const response = await fetch(url, { signal: controller.signal });
            clearTimeout(timer);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const text = await response.text();
            [...text.matchAll(/\{\*(.*?)\*\}/g)].forEach((m, i) =>
                console.log(`Secret #${i + 1}: ${m[1].trim()}`)
            );
            return;
        } catch (err) {
            lastError = err;
            const wait = BASE_DELAY_MS * Math.pow(2, attempt - 1);
            console.warn(
                `Attempt ${attempt}/${MAX_RETRIES} failed: ${err.message}. Retrying in ${wait}ms...`
            );
            await new Promise((r) => setTimeout(r, wait));
        }
    }
    console.error(`All ${MAX_RETRIES} attempts failed. Last error: ${lastError?.message}`);
}

const blueprintUrl = "https://raw.githubusercontent.com/microsoft/CopilotAdventures/main/Data/scrolls.txt";
retrieveAndDecodeBlueprint(blueprintUrl).catch((err) => {
    console.error(`Mission failed: ${err.message}`);
    process.exit(1);
});
