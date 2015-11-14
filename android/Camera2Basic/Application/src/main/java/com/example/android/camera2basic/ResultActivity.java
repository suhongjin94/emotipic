package com.example.android.camera2basic;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.media.ExifInterface;
import android.os.Bundle;
import android.widget.ImageView;

import java.io.IOException;

/**
 * Created by suhon_000 on 11/14/2015.
 */
public class ResultActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);
        String path = getIntent().getStringExtra("TESTING");
        Bitmap bitmap = BitmapFactory.decodeFile(path);
        bitmap = rotateImage(bitmap, 270);
//        try {
//            ExifInterface ei = new ExifInterface(path);
//            int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);
//
//            switch(orientation) {
//                case ExifInterface.ORIENTATION_ROTATE_90:
//                    bitmap = rotateImage(bitmap, 90);
//                    break;
//                case ExifInterface.ORIENTATION_ROTATE_180:
////                    bitmap = rotateImage(bitmap, 180);
//                    break;
//                // etc.
//            }
//        } catch (IOException e) {
//
//        }

        ImageView img = (ImageView) findViewById(R.id.result_image);
        img.setImageBitmap(bitmap);
    }

    private Bitmap rotateImage(Bitmap source, float angle)
    {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(), matrix, true);
    }
}
