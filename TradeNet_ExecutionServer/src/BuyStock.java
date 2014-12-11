import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.sql.SQLException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


public class BuyStock extends HttpServlet
{
  public static String status = "";

  protected void doGet(HttpServletRequest request, HttpServletResponse response)
          throws ServletException, IOException
  {
    String stock = request.getParameter("stock");
    DataAccess dataAccess = null;
    try
    {

      double sharePrice = Tradier.getStockQuote(stock);
      if (status.equals(""))
      {

        dataAccess = new DataAccess();
        double accountBalance = 0;

        String custId = request.getParameter("custId");
        try
        {
          dataAccess.open();
          accountBalance = dataAccess.getAccountBalance(custId);
        } catch (SQLException e)
        {
          status = "OOPS! Something went wrong! Error 1 " + e.getMessage();
          dataAccess.close();
          return;
        }
        int shares = Integer.parseInt(request.getParameter("shares"));
        double totalSharePrice = round(shares * sharePrice, 2);
        if (accountBalance < totalSharePrice && status.equals(""))
        {
          status = "Insufficient funds for this transaction.";
        }
        else if (status.equals(""))
        {
          dataAccess.createTranaction(custId, stock, shares, totalSharePrice);
          dataAccess.updatePortfolio(custId, stock, shares, totalSharePrice);
          dataAccess.updateBalance(custId, totalSharePrice);
          status = "Transaction was successful.";
        }
      }
    } catch (SQLException e)
    {
      status = "OOPS! Something went wrong! Error 3" + e.getMessage();
    } finally
    {
      if (dataAccess != null)
      {
        try
        {
          dataAccess.close();
        } catch (SQLException e)
        {
          e.printStackTrace();
        }
      }
    }


    JSONObject responseJson = new JSONObject();
    try
    {
      responseJson.put("success", status);
    } catch (JSONException e)
    {
      status = "OOPS! Something went wrong! Error 4";
    }
    String jsonText = responseJson.toString();
    response.getWriter().print(jsonText);
  }
  public static double round(double value, int places) {
    if (places < 0) throw new IllegalArgumentException();

    BigDecimal bd = new BigDecimal(value);
    bd = bd.setScale(places, RoundingMode.HALF_UP);
    return bd.doubleValue();
  }
}
