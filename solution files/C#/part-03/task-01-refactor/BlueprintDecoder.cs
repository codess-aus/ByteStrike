using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;

public class BlueprintDecoder
{
    private static readonly Regex SecretPattern = new Regex(@"\{\* (.*?) \*\}", RegexOptions.Compiled);

    /// <summary>Read and return the raw content of a blueprint file.</summary>
    public static string ReadBlueprint(string filename) => File.ReadAllText(filename);

    /// <summary>Extract all secrets marked between {* and *} from content.</summary>
    public static List<string> ExtractSecrets(string content) =>
        SecretPattern.Matches(content)
                     .Select(m => m.Groups[1].Value)
                     .ToList();

    /// <summary>Count secrets by their category prefix (text before the first colon).</summary>
    public static Dictionary<string, int> CategorizeSecrets(List<string> secrets) =>
        secrets.GroupBy(s => s.Contains(':') ? s.Split(':')[0].Trim() : "UNKNOWN")
               .ToDictionary(g => g.Key, g => g.Count());

    /// <summary>Full pipeline: read file safely and extract secrets.</summary>
    public static List<string> DecodeBlueprintSafe(string filename)
    {
        try { return ExtractSecrets(ReadBlueprint(filename)); }
        catch (FileNotFoundException) { System.Console.WriteLine($"Error: '{filename}' not found."); return new(); }
    }
}
