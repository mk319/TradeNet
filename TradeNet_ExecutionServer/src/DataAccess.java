import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import sun.jdbc.odbc.ee.DataSource;


/**
 * Created by Matt on 12/9/2014.
 */
public class DataAccess
{

  private Connection        connection        = null;
  private Statement         statement         = null;
  private PreparedStatement preparedStatement = null;
  private ResultSet         resultSet         = null;

  public void open() throws SQLException
  {
    try
    {
      Class.forName("com.mysql.jdbc.Driver");
    } catch (ClassNotFoundException e)
    {
      BuyStock.status = "OOPS! Something went wrong! Error 10";
    }

    connection = DriverManager.getConnection("jdbc:mysql://localhost/jew411?" +
                                             "user=jew411&password=jew411");
  }

  public void close() throws SQLException
  {
    if (connection != null)
      connection.close();
  }

  public double getAccountBalance(String custId) throws SQLException
  {


    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String select = "SELECT accountbalance FROM `Customer Info` WHERE custId=?";
    // resultSet gets the result of the SQL query
    preparedStatement = connection.prepareStatement(select);
    preparedStatement.setString(1, custId);
    resultSet = preparedStatement.executeQuery();

    if (!resultSet.first())
    {
      BuyStock.status = "Customer could not be found.";
      return 0;
    }
    else
    {
      BuyStock.status = "";
    }

    double accountBalance = Double.parseDouble(resultSet.getString("accountbalance"));

    preparedStatement.close();
    statement.close();
    return accountBalance;
  }


  public void createTranaction(String custId, String stock, int shares, double purchasePrice)
          throws SQLException
  {
    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String insertString = "INSERT INTO jew411.Transactions (custId, stock, shares, purchaseprice) "
                          + "VALUES (?, ?, ?, ?)";
    preparedStatement = connection.prepareStatement(insertString);

    preparedStatement.setString(1, custId);
    preparedStatement.setString(2, stock);
    preparedStatement.setInt(3, shares);
    preparedStatement.setDouble(4, purchasePrice);
    preparedStatement.executeUpdate();

    preparedStatement.close();
    statement.close();
  }

  public void updatePortfolio(String custId, String stock, int shares, double purchasePrice) throws
          SQLException
  {
    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String insertString = "INSERT INTO jew411.Portfolio (custId, stock, shares, purchaseprice)"
                          + " VALUES (?, ?, ?, ?)"
                          + " ON DUPLICATE KEY UPDATE"
                          + " shares = shares + ?,"
                          + " purchaseprice = purchaseprice + ?";
    preparedStatement = connection.prepareStatement(insertString);

    preparedStatement.setString(1, custId);
    preparedStatement.setString(2, stock);
    preparedStatement.setInt(3, shares);
    preparedStatement.setDouble(4, purchasePrice);
    preparedStatement.setInt(5, shares);
    preparedStatement.setDouble(6, purchasePrice);

    preparedStatement.executeUpdate();

    preparedStatement.close();
    statement.close();
  }

  public void updateBalance(String custId, double purchasePrice) throws SQLException
  {
    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String insertString = "UPDATE jew411.`Customer Info` SET accountbalance = accountbalance - ?"
                          + " WHERE custId = ?";
    preparedStatement = connection.prepareStatement(insertString);
    preparedStatement.setDouble(1, purchasePrice);
    preparedStatement.setString(2, custId);
    preparedStatement.executeUpdate();

    preparedStatement.close();
    statement.close();
  }

  public boolean isEnoughShares(String custId, String stock, int shares) throws SQLException
  {
    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String select = "SELECT shares FROM Portfolio WHERE custId=? AND stock=?";
    // resultSet gets the result of the SQL query
    preparedStatement = connection.prepareStatement(select);
    preparedStatement.setString(1, custId);
    preparedStatement.setString(2, stock);
    resultSet = preparedStatement.executeQuery();
    if (resultSet.first())
    {
      int currentShares = resultSet.getInt(1);
      preparedStatement.close();
      statement.close();
      return currentShares >= shares;
    }
    else
    {
      preparedStatement.close();
      statement.close();
      return false;
    }
  }

  public JSONArray getTransactions(String custId) throws SQLException, JSONException
  {
    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String select = "SELECT * FROM Transactions WHERE custId=?";
    // resultSet gets the result of the SQL query
    preparedStatement = connection.prepareStatement(select);
    preparedStatement.setString(1, custId);
    preparedStatement.execute();
    resultSet = preparedStatement.getResultSet();
    JSONArray jsonArray = new JSONArray();

    while (resultSet.next())
    {
      JSONObject jsonObject = new JSONObject();
      jsonObject.put("stock", resultSet.getString("stock"));
      jsonObject.put("shares", resultSet.getInt("shares"));
      jsonObject.put("datetime", resultSet.getTimestamp("datetime"));
      jsonObject.put("purchaseprice", resultSet.getDouble("purchaseprice"));
      jsonArray.put(jsonObject);
    }
    preparedStatement.close();
    statement.close();
    return jsonArray;

  }

  public JSONArray getPortfolio(String custId) throws SQLException, JSONException
  {
    // statements allow to issue SQL queries to the database
    statement = connection.createStatement();

    String select = "SELECT * FROM Portfolio WHERE custId=?";
    // resultSet gets the result of the SQL query
    preparedStatement = connection.prepareStatement(select);
    preparedStatement.setString(1, custId);
    preparedStatement.execute();
    resultSet = preparedStatement.getResultSet();
    JSONArray jsonArray = new JSONArray();

    while (resultSet.next())
    {
      JSONObject jsonObject = new JSONObject();
      jsonObject.put("stock", resultSet.getString("stock"));
      jsonObject.put("shares", resultSet.getInt("shares"));
      jsonObject.put("purchaseprice", resultSet.getDouble("purchaseprice"));
      jsonArray.put(jsonObject);
    }
    preparedStatement.close();
    statement.close();
    return jsonArray;
  }
}
