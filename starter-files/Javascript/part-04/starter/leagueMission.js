async function retrieveAndDecodeBlueprint(url) {
    try {
        console.log(`Starting League mission: ${url}`);
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Fetch error: ${response.status}`);

        const secretPattern = /\{\*(.*?)\*\}/g;
        const text = await response.text();
        const secrets = [...text.matchAll(secretPattern)].map((m) => m[1].trim());

        console.log("=== LEAGUE MISSION DOSSIER ===");
        if (secrets.length) {
            secrets.forEach((s, i) => console.log(`Secret #${i + 1}: ${s}`));
        } else {
            console.log("No League secrets found. All data may be decoys!");
        }
    } catch (error) {
        console.error("[ALERT] Mission error:", error);
    }
}

// Run the mission
const url = "https://raw.githubusercontent.com/codess-aus/AI-Assisted-Dev-with-GitHub-Copilot/main/blueprint-data.txt";
retrieveAndDecodeBlueprint(url);
