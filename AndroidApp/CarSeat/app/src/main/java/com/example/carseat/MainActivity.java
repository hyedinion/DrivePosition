package com.example.carseat;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import app.akexorcist.bluetotohspp.library.BluetoothSPP;

public class MainActivity extends AppCompatActivity {
    DBHelper helper;
    SQLiteDatabase db;
    String name = "hyejin";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        helper = new DBHelper(MainActivity.this, "newdb.db", null, 1);
        db = helper.getWritableDatabase();
        helper.onCreate(db);
        Toast.makeText(getApplicationContext(), "create", Toast.LENGTH_SHORT).show();

    }

    public void onClick(View view) {


        switch(view.getId())
        {
            //저장 버튼을 눌렀을 때
            case R.id.saveButton:
                //데이터 요청
                ((BluetoothActivity)BluetoothActivity.context).bt.send("0", true);
                //데이터 받기
                ((BluetoothActivity)BluetoothActivity.context).bt.setOnDataReceivedListener(new BluetoothSPP.OnDataReceivedListener() { //데이터 수신
                    public void onDataReceived(byte[] data, String message) {
                        String sql;
                        Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();

                        Cursor c2 = db.rawQuery("select * from mytable",null);
                        int cnt = c2.getCount();

                        //insert
                        if (cnt ==0){
                            sql = "INSERT INTO  mytable('_id','seat')  values('" +name+ "','" +message+ "');" ;
                            db.execSQL(sql);
                            System.out.println("insert");
                        }
                        //update
                        else{
                            ContentValues values = new ContentValues();
                            values.put("seat",message);
                            db.update("mytable",values,"_id=?",new String[]{name});

                            sql = "select * from mytable;";
                            Cursor c = db.rawQuery(sql, null);

                            //확인 log
                            while(c.moveToNext()){
                                System.out.println("test");
                                System.out.println("_id : "+c.getString(c.getColumnIndex("_id")));
                                System.out.println("seat : "+c.getString(c.getColumnIndex("seat")));
                                System.out.println("testfinish");
                            }

                        }
                    }


                });

                Toast.makeText(getApplicationContext(), "save", Toast.LENGTH_SHORT).show();


                break;





            //적용버튼을 눌렀을 때
            case R.id.applyButton:
                String sql;

                sql = "select seat from mytable where _id='" +name+ "';";
                Cursor c = db.rawQuery(sql, null);
                while(c.moveToNext()){
                    //데이터 보내기
                    String data = "1 "+c.getString(0)+"\n";
                    ((BluetoothActivity)BluetoothActivity.context).bt.send(data, true);
                    System.out.println("seat : "+c.getString(0));
                }

                Toast.makeText(getApplicationContext(), "apply", Toast.LENGTH_SHORT).show();
                break;
        }
    }
}