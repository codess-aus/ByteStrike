const { validateUrl } = require("./urlValidation");

test("valid HTTPS URL passes", () => {
    expect(() =>
        validateUrl(
            "https://raw.githubusercontent.com/microsoft/CopilotAdventures/main/Data/scrolls.txt"
        )
    ).not.toThrow();
});

test("HTTP URL is blocked", () => {
    expect(() => validateUrl("http://raw.githubusercontent.com/some/path")).toThrow(
        "must use HTTPS"
    );
});

test("unknown host is blocked", () => {
    expect(() => validateUrl("https://evil.example.com/payload")).toThrow(
        "not in the allowed list"
    );
});
