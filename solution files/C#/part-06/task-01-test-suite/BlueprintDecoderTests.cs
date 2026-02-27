using Xunit;
using Moq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

public class BlueprintDecoderTests
{
    private readonly BlueprintDecoder _decoder = new BlueprintDecoder();

    [Fact]
    public void ValidateUrl_WithWhitelistedUrl_ReturnsTrue()
    {
        // Arrange
        string validUrl = "https://internal.company.com/blueprints/data.txt";

        // Act
        bool result = _decoder.ValidateUrl(validUrl);

        // Assert
        Assert.True(result);
    }

    [Fact]
    public void ValidateUrl_WithBlacklistedUrl_ReturnsFalse()
    {
        // Arrange
        string invalidUrl = "https://evil.com/malware.txt";

        // Act
        bool result = _decoder.ValidateUrl(invalidUrl);

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void ExtractSecrets_WithValidMarkers_ReturnsSecrets()
    {
        // Arrange
        string content = "Some data {* SECRET_CODE: ALPHA-123 *} more data";

        // Act
        var secrets = _decoder.ExtractSecrets(content);

        // Assert
        Assert.Single(secrets);
        Assert.Equal("SECRET_CODE: ALPHA-123", secrets[0]);
    }

    [Fact]
    public void ExtractSecrets_WithMultipleSecrets_ReturnsAll()
    {
        // Arrange
        string content = "{* SECRET1 *} data {* SECRET2 *} more {* SECRET3 *}";

        // Act
        var secrets = _decoder.ExtractSecrets(content);

        // Assert
        Assert.Equal(3, secrets.Count);
    }

    [Fact]
    public void ExtractSecrets_WithNoSecrets_ReturnsEmpty()
    {
        // Arrange
        string content = "Just regular data, no secrets here";

        // Act
        var secrets = _decoder.ExtractSecrets(content);

        // Assert
        Assert.Empty(secrets);
    }

    [Fact]
    public void ExtractSecrets_WithMalformedMarkers_OnlyExtractsValid()
    {
        // Arrange
        string content = "{* INCOMPLETE MARKER only start, or } INCOMPLETE END {* VALID *}";

        // Act
        var secrets = _decoder.ExtractSecrets(content);

        // Assert
        Assert.Single(secrets);
        Assert.Equal("VALID", secrets[0]);
    }

    [Fact]
    public async Task DecodeBlueprintSafe_WithTimeout_ReturnsEmpty()
    {
        // Arrange
        // Mock HTTP client to throw timeout
        var mockClient = new Mock<HttpClient>();
        mockClient.Setup(c => c.GetAsync(It.IsAny<string>(), It.IsAny<HttpCompletionOption>()))
            .ThrowsAsync(new TaskCanceledException("Request timed out"));

        // Act
        var result = await _decoder.DecodeBlueprintSafeAsync("https://internal.company.com/data.txt");

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void ExtractSecrets_WithLargeInput_HandlesEfficiently()
    {
        // Arrange
        var content = string.Concat(Enumerable.Range(0, 1000)
            .Select(i => $"{{* SECRET_{i} *}} "));

        // Act
        var secrets = _decoder.ExtractSecrets(content);

        // Assert
        Assert.Equal(1000, secrets.Count);
    }

    [Fact]
    public void ErrorMessages_DoNotLogSecrets()
    {
        // Arrange
        string contentWithSecret = "{* CONFIDENTIAL_DATA *} something {* ANOTHER_SECRET *}";

        // Act
        try
        {
            _decoder.ProcessWithValidation(contentWithSecret, "invalid-url");
        }
        catch (Exception ex)
        {
            // Assert: Error message should not contain extracted secrets
            Assert.DoesNotContain("CONFIDENTIAL_DATA", ex.Message);
            Assert.DoesNotContain("ANOTHER_SECRET", ex.Message);
        }
    }
}
