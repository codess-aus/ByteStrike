using System;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

public class LeagueHQ
{
    private static readonly HttpClient _client = new() { Timeout = TimeSpan.FromSeconds(10) };
    private static readonly Regex _pattern = new(@"\{\*(.*?)\*\}", RegexOptions.Compiled);
    private const int MaxRetries = 3;

    private static async Task RetrieveAndDecodeBlueprint(string url)
    {
        Exception? lastError = null;
        for (int attempt = 1; attempt <= MaxRetries; attempt++)
        {
            try
            {
                var content = await _client.GetStringAsync(url);
                var matches = _pattern.Matches(content);
                for (int i = 0; i < matches.Count; i++)
                    Console.WriteLine($"Secret #{i + 1}: {matches[i].Groups[1].Value.Trim()}");
                return;
            }
            catch (HttpRequestException e)
            {
                lastError = e;
                int wait = (int)Math.Pow(2, attempt - 1);
                Console.Error.WriteLine(
                    $"Attempt {attempt}/{MaxRetries} failed: {e.Message}. Retrying in {wait}s..."
                );
                await Task.Delay(wait * 1000);
            }
        }
        Console.Error.WriteLine($"All {MaxRetries} attempts failed. Last error: {lastError?.Message}");
    }

    public static async Task Main()
    {
        const string blueprintUrl = "https://raw.githubusercontent.com/microsoft/CopilotAdventures/main/Data/scrolls.txt";
        await RetrieveAndDecodeBlueprint(blueprintUrl);
    }
}
