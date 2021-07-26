package com.example.driveposition2;

import android.app.Application;

import java.net.URISyntaxException;

import io.socket.client.IO;
import io.socket.client.Socket;

public class socketApplication extends Application {
    private Socket mSocket;
    {
        try {
            //python-engineio==3.13.2 and python-socketio==4.6.0
            mSocket = IO.socket("http://192.168.137.148:5000");
            mSocket.connect();
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }

    public Socket getSocket() {
        return mSocket;
    }
}
