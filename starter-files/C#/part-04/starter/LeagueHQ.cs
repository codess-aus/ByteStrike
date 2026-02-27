using System;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

public class LeagueHQ
{
    private static async Task RetrieveAndDecodeBlueprint(string url)
    {
        Console.WriteLine($"Initiating League mission: {url}");
        try
        {
            using var httpClient = new HttpClient();
            var blueprintContent = await httpClient.GetStringAsync(url);

            var secretPattern = new Regex(@"\{\*(.*?)\*\}");
            var matches = secretPattern.Matches(blueprintContent);

            Console.WriteLine("=== LEAGUE MISSION DOSSIER ===");
            if (matches.Count == 0)
            {
                Console.WriteLine("No League secrets found. All data may be decoys!");
                return;
            }

            int count = 1;
            foreach (Match match in matches)
            {
                Console.WriteLine($"Secret #{count}: {match.Groups[1].Value.Trim()}");
                count++;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ALERT] Operation error: {ex.Message}");
        }
    }

    public static async Task Main()
    {
        const string url = "https://raw.githubusercontent.com/codess-aus/AI-Assisted-Dev-with-GitHub-Copilot/main/blueprint-data.txt";
        await RetrieveAndDecodeBlueprint(url);
    }
}
