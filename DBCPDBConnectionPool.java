package dataLayer;


import org.apache.commons.dbcp.BasicDataSource;

import java.sql.Connection;
import java.sql.SQLException;

/**
 *
 * do not reinvent the wheel!!!
 *
 * you can use DBCP or other libraries.
 *
 * @see <a href="https://www.baeldung.com/java-connection-pooling">A Simple Guide to Connection Pooling in Java</a>
 *
 * */
public class DBCPDBConnectionPool {

    private static BasicDataSource ds = new BasicDataSource();
    private final static String dbURL = "jdbc:sqlite:taca7.db";

    static {
        ds.setUrl(dbURL);
        ds.setMinIdle(1);
        ds.setMaxIdle(2);
    }

    public static Connection getConnection() throws SQLException {
        return ds.getConnection();
    }

    private DBCPDBConnectionPool(){ }
}
