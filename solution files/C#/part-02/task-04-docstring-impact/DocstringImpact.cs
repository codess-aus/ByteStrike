using System;

public class DocstringImpact
{
    /// <summary>
    /// Calculate the area of a triangle given three side lengths using Heron's formula.
    /// </summary>
    /// <param name="a">Length of side A</param>
    /// <param name="b">Length of side B</param>
    /// <param name="c">Length of side C</param>
    /// <returns>The area of the triangle</returns>
    public double Calculate(double a, double b, double c)
    {
        double s = (a + b + c) / 2;
        return Math.Sqrt(s * (s - a) * (s - b) * (s - c));
    }
}
