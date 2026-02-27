// Example: ["alice", "bob"] -> ["ALICE", "BOB"]
const formatNames = (names) => names.map((name) => name.toUpperCase());

// Using the same pattern as formatNames above:
// Example: ["2026-01-17", "2026-02-20"] -> ["Jan 17, 2026", "Feb 20, 2026"]
const formatDates = (dates) => {
    return dates.map((d) =>
        new Date(d).toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric",
        })
    );
};

module.exports = { formatNames, formatDates };
