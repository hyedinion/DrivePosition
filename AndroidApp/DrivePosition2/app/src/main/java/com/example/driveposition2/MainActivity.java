package com.example.driveposition2;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URISyntaxException;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;

public class MainActivity extends AppCompatActivity {

    private Socket mSocket;
    String intentString;
    DBHelper helper;
    SQLiteDatabase db;
    Integer id = 1242134;
    Integer height = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        socketApplication app = (socketApplication) getApplication();
        mSocket = app.getSocket();

        mSocket.on("save_send", save_send);
        mSocket.on("disconnected", disconnected);
        intentString = getIntent().getStringExtra("data");
        height = Integer.parseInt(getIntent().getStringExtra("height"));

        //db연결
        helper = new DBHelper(MainActivity.this, "newdb.db", null, 1);
        db = helper.getWritableDatabase();
        helper.onCreate(db);


    }

    public void onClick(View view) {
        switch(view.getId())
        {
            //저장 버튼을 눌렀을 때
            case R.id.saveButton:
                mSocket.emit("save_request","save_request" );
                Toast.makeText(getApplicationContext(), "save", Toast.LENGTH_SHORT).show();
                break;

            //적용버튼을 눌렀을 때
            case R.id.applyButton:
                String sql;
                String drivepos = null;
                sql = "select drivepos from mytable where id='" +id+ "';";
                Cursor c = db.rawQuery(sql, null);
                int cnt = c.getCount();
                //save를 먼저 안했을 때
                if (cnt==0){
                    Toast.makeText(getApplicationContext(), "save first", Toast.LENGTH_SHORT).show();
                }
                else{
                    sql = "select * from mytable where id='" +id+ "';";
                    c = db.rawQuery(sql, null);
                    while(c.moveToNext()){
                        //데이터 보내기
                        drivepos = c.getString(1);
                        height = c.getInt(2);
                    }
                    mSocket.emit("apply",drivepos);
                    Toast.makeText(getApplicationContext(), "apply", Toast.LENGTH_SHORT).show();
                }

                break;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mSocket.off("save_send", save_send);
        mSocket.off("disconnected", disconnected);
    }

    private Emitter.Listener save_send = new Emitter.Listener() {
        @Override
        public void call(Object... args) {
            String s = args[0].toString();

            String sql;
            Cursor c2 = db.rawQuery("select * from mytable",null);
            int cnt = c2.getCount();
            //insert
            if (cnt ==0){
                sql = "INSERT INTO  mytable('id','drivepos','height')  values('" +id+ "','" +s+ "','" +height+ "');" ;
                db.execSQL(sql);
                System.out.println("insert");
                MainActivity.this.runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(MainActivity.this, "insert", Toast.LENGTH_SHORT).show();
                    }
                });
            }
            //update
            else{
                ContentValues values = new ContentValues();
                values.put("drivepos",s);
                db.update("mytable",values,"id=?",new String[]{id.toString()});
                MainActivity.this.runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(MainActivity.this, "update", Toast.LENGTH_SHORT).show();
                    }
                });
            }
        }
    };

    private Emitter.Listener disconnected = new Emitter.Listener() {
        @Override
        public void call(Object... args) {
            finish();
        }
    };



}