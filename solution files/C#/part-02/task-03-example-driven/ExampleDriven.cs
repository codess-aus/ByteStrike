using System;
using System.Collections.Generic;
using System.Linq;

public class ExampleDriven
{
    public List<string> FormatNames(List<string> names)
    {
        // Example: ["alice", "bob"] -> ["ALICE", "BOB"]
        return names.Select(n => n.ToUpper()).ToList();
    }

    public List<string> FormatDates(List<string> dates)
    {
        // Using the same pattern as FormatNames above:
        // Example: ["2026-01-17", "2026-02-20"] -> ["Jan 17, 2026", "Feb 20, 2026"]
        return dates.Select(d => DateTime.Parse(d).ToString("MMM dd, yyyy")).ToList();
    }
}
