package zy;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.TableName;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.HTableDescriptor;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        Configuration conf = HBaseConfiguration.create();
        //conf.set("hbase.rootdir", "hdfs://192.168.56.4:9000/hbase");
        conf.set("hbase.zookeeper.quorum", "192.168.56.4,192.168.56.5,192.168.56.6");

        Connection conn = null;

        Admin admin = null;

        try {
            conn = ConnectionFactory.createConnection(conf);
            admin = conn.getAdmin();
        }catch(IOException e){
            e.printStackTrace();
        }

        String TABLE_NAME = "test2";
        String COLUMN_FAMILY_NAME1 = "columnfamily1";
        String COLUMN_FAMILY_NAME2 = "columnfamily2";

        String [] COLUMNS = {"column0", "column1", "column2"};

        String ROW_KEYS = "row0";

        String[] VALUES = {"value0", "value1", "value2"};

        System.out.println("CREATE TABLE ======");

        TableName tableName = TableName.valueOf(TABLE_NAME);

        try{
            if(admin.tableExists(tableName)) {
                admin.disableTable(tableName);
                admin.deleteTable(tableName);
            }
            HTableDescriptor descriptor = new HTableDescriptor(tableName);

            descriptor.addFamily(new HColumnDescriptor(COLUMN_FAMILY_NAME1));
            descriptor.addFamily(new HColumnDescriptor(COLUMN_FAMILY_NAME2));

            System.out.println("Creating the table");
            admin.createTable(descriptor);
            System.out.println("Table created");
        }catch(IOException e){
            e.printStackTrace();
        }

        try{
            Table table = conn.getTable(tableName);
            Put put = new Put(ROW_KEYS.getBytes());
            put.addColumn(COLUMN_FAMILY_NAME1.getBytes(), COLUMNS[0].getBytes(), VALUES[0].getBytes());
            put.addColumn(COLUMN_FAMILY_NAME1.getBytes(), COLUMNS[1].getBytes(), VALUES[1].getBytes());
            put.addColumn(COLUMN_FAMILY_NAME1.getBytes(), COLUMNS[2].getBytes(), VALUES[2].getBytes());
            table.put(put);
            table.close();
        }catch(IOException e){
            e.printStackTrace();
        }

        try{
            Table table = conn.getTable(tableName);
            //Put put = new Put(ROW_KEYS.getBytes());
            Get get = new Get(ROW_KEYS.getBytes());
            Result result = table.get(get);
            System.out.println("Get: " + result);
            table.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }
}
