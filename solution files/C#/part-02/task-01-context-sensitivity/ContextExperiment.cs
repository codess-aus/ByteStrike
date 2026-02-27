using System.Collections.Generic;
using System.Linq;

public class ContextExperiment
{
    public List<string> ExtractNames(List<Dictionary<string, object>> data)
    {
        // Extract the 'name' field from each dictionary and return as a list of strings
        return data.Select(d => d["name"].ToString()).ToList();
    }
}
