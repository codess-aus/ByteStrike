using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;

public class BlueprintDecoder
{
    private static readonly Regex SecretPattern = new Regex(@"\{\* (.*?) \*\}", RegexOptions.Compiled);

    /// <summary>Read and return the raw content of a blueprint file.</summary>
    public static string ReadBlueprint(string filename) => File.ReadAllText(filename);

    /// <summary>
    /// Extracts all secrets marked between {* and *} delimiters from a string.
    /// Searches the given content for all occurrences of the pattern {* ... *}
    /// and returns the captured groups.
    /// </summary>
    /// <param name="content">
    /// The raw text to search. May contain zero or more secret markers.
    /// </param>
    /// <returns>
    /// A list of extracted secret strings in the order they appear.
    /// Returns an empty list if no markers are found.
    /// </returns>
    /// <example>
    /// <code>
    /// var secrets = ExtractSecrets("data {* VAULT_CODE: DELTA-7 *} end");
    /// // secrets == ["VAULT_CODE: DELTA-7"]
    /// </code>
    /// </example>
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
