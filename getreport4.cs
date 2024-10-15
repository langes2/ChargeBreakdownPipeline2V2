using System;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;

class Apitester
{
    static async Task Main(string[] args)
    {
        // Fetch the API token using TokenFetcher
        TokenFetcher tokenFetcher = new TokenFetcher();
        string apiToken = await tokenFetcher.GetApiToken();

        if (string.IsNullOrEmpty(apiToken))
        {
            Console.WriteLine("Failed to retrieve API token.");
            return;
        }
        
        // Initialize HttpClient
        using (HttpClient client = new HttpClient())
        {
            client.Timeout = TimeSpan.FromMinutes(15);
            client.BaseAddress = new Uri("https://della.api.rentmanager.com/");

            // Set up the request headers
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            client.DefaultRequestHeaders.Add("X-RM12Api-ApiToken", apiToken);
            client.DefaultRequestHeaders.Add("X-RM12Api-locationID", "4");

            // Get first of month date and current date
            // Automatically fill in the first of the current month
            DateTime firstDayOfPreviousMonth = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1).AddMonths(-1);
            // Automatically fill in the last day of the previous month
            DateTime lastDayOfPreviousMonth = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1).AddDays(-1);

            string startDate = firstDayOfPreviousMonth.ToString("MM/dd/yy");
            string endDate = lastDayOfPreviousMonth.ToString("MM/dd/yy");

            HttpResponseMessage response = await client.GetAsync($"/Reports/29/RunReport?parameters=ChargeTypeOrder,(81,82,83,84,85,86,87,88,89,90,91,92);StartDate,{startDate};EndDate,{endDate}&GetOptions=ReturnExcelStream");
            try
            {
                response.EnsureSuccessStatusCode();
            }
            catch (HttpRequestException ex)
            {
                if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                return;
                }
                else
                {
                throw ex;
                }
            }
            
            string useDate = lastDayOfPreviousMonth.ToString("MM_dd_yy");

            string reportPath = $@"C:\Users\Public\Documents\CBfrags\CBfragsmonthly{useDate}";
            Directory.CreateDirectory(reportPath); // Ensure the directory exists
            //string reportPath = r"C:\Users\Public\Documents\ChargeBreakdowns"
            string reportFile = Path.Combine(reportPath, $"ChargeBreakdown{useDate}frag4.xlsx");

            //string reportPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            //string reportFile = reportPath + $@"\ChargeBreakdown{currDate}.xlsx";

            Stream reportStream = response.Content.ReadAsStreamAsync().Result;
            if (reportStream.GetType().Name == "MemoryStream")
            {
                if (File.Exists(reportFile))
                {
                File.Delete(reportFile);
                }

                Stream fileStream = File.Create(reportFile);
                reportStream.CopyTo(fileStream);

                fileStream.Close();
                reportStream.Close();
            }
        }
    }
}
