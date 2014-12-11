import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.SQLException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.crypto.Data;

/**
 * Created by Matt on 12/10/2014.
 */
public class SellStock extends HttpServlet
{
  protected void doGet(HttpServletRequest request,
                       HttpServletResponse response)
          throws ServletException, IOException
  {
    String stock = request.getParameter("stock");
    String custId = request.getParameter("custId");
    int shares = Integer.parseInt(request.getParameter("shares"));

    //check if custId has enough shares of stock
    DataAccess dataAccess = new DataAccess();
    try
    {
      dataAccess.open();
      if(dataAccess.isEnoughShares(custId, stock, shares))
      {
        //get stock quote from tradier
        double stockPrice = Tradier.getStockQuote(stock);
        double totalStockPrice = BuyStock.round(stockPrice*shares,2);
        //update balance, portfolio, and transactions
        dataAccess.updateBalance(custId, -totalStockPrice);
        dataAccess.updatePortfolio(custId, stock, -shares, -totalStockPrice);
        dataAccess.createTranaction(custId, stock, -shares, -totalStockPrice);
        BuyStock.status = "Transaction was successful.";
      }
      else {
        BuyStock.status = "Customer does not exists or you do not have enough shares of this "
                          + "stock.";
      }
    } catch (SQLException e)
    {
      e.printStackTrace();
    }
    finally
    {
      try
      {
        dataAccess.close();
      } catch (SQLException e)
      {
        e.printStackTrace();
      }
    }
    JSONObject responseJson = new JSONObject();
    try
    {
      responseJson.put("success", BuyStock.status);
    } catch (JSONException e)
    {
      BuyStock.status = "OOPS! Something went wrong! Error 4";
    }
    String jsonText = responseJson.toString();
    response.getWriter().print(jsonText);

  }
}
