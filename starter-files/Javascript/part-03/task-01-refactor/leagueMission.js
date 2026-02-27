function decodeBlueprint(filename) {
    try {
        const content = require("fs").readFileSync(filename, "utf8");
        const secrets = [...content.matchAll(/\{\* (.*?) \*\}/g)].map((m) => m[1]);
        console.log("=".repeat(40));
        console.log("DECODED SECRETS REPORT");
        console.log("=".repeat(40));
        console.log(`Found ${secrets.length} secret(s):\n`);
        secrets.forEach((s, i) => console.log(`${i + 1}. ${s}`));
        console.log("=".repeat(40));
        const cats = {};
        for (const s of secrets) {
            const key = s.includes(":") ? s.split(":")[0].trim() : "UNKNOWN";
            cats[key] = (cats[key] ?? 0) + 1;
        }
        return cats;
    } catch (err) {
        console.log(`Error: '${filename}' not found.`);
        return {};
    }
}
