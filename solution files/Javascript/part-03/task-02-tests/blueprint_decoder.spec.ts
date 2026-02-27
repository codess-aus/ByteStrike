import { test, expect } from "@playwright/test";
import { extractSecrets, categorizeSecrets } from "./leagueMission";

test.describe("extractSecrets", () => {
    test("finds all secrets", () => {
        const content = "data {* SECRET_ONE *} more {* KEY: VALUE *} end";
        expect(extractSecrets(content)).toEqual(["SECRET_ONE", "KEY: VALUE"]);
    });

    test("returns empty array when no matches", () => {
        expect(extractSecrets("no secrets here")).toEqual([]);
    });

    test("handles empty string", () => {
        expect(extractSecrets("")).toEqual([]);
    });
});

test.describe("categorizeSecrets", () => {
    test("groups secrets by prefix", () => {
        const secrets = [
            "AGENT_CODENAME: SHADOWMIND",
            "VAULT_ACCESS_CODE: DELTA-7",
            "AGENT_CODENAME: GHOSTFIRE",
        ];
        expect(categorizeSecrets(secrets)).toEqual({ AGENT_CODENAME: 2, VAULT_ACCESS_CODE: 1 });
    });

    test("marks secrets without colon as UNKNOWN", () => {
        expect(categorizeSecrets(["SECURE_COMMS_PROTOCOL"]).UNKNOWN).toBe(1);
    });

    test("returns empty object for empty array", () => {
        expect(categorizeSecrets([])).toEqual({});
    });
});
