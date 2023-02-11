package com.aminbeheshti.exifviewer

import android.annotation.SuppressLint
import android.content.*
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.database.Cursor
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.provider.OpenableColumns
import android.util.Log
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.exifinterface.media.ExifInterface
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.BasicNetwork
import com.android.volley.toolbox.DiskBasedCache
import com.android.volley.toolbox.HurlStack
import com.android.volley.toolbox.JsonObjectRequest
import com.google.android.material.textfield.TextInputLayout
import java.io.*
import java.lang.String.format
import java.util.*


class MainActivity : AppCompatActivity() {

    private val TAG = "MainActivity"

    companion object {
        private const val PICK_PHOTO_CODE = 655
        private const val READ_EXTERNAL_PHOTOS_CODE = 248
        private const val READ_PHOTO_PERMISSION = android.Manifest.permission.READ_EXTERNAL_STORAGE
    }

    lateinit var imageView: ImageView
    private lateinit var button: Button
    private lateinit var btnCopyAll: Button

    private var imageUri: Uri? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        title = "Exif Viewer"

        // get the package info instance
        val packageInfo: PackageInfo = packageManager.getPackageInfo(packageName, 0)
        // get this app version name programmatically
        val versionName: String = packageInfo.versionName

        imageView = findViewById(R.id.imageView)
        imageView.setImageResource(R.drawable.ic_select_img)
        button = findViewById(R.id.buttonLoadPicture)
        button.setOnClickListener {
            if (isPermissionGranted(this@MainActivity, READ_PHOTO_PERMISSION)) {
                launchIntentForPhotos()
            } else {
                requestPermission(
                        this@MainActivity,
                        READ_PHOTO_PERMISSION,
                        READ_EXTERNAL_PHOTOS_CODE
                )
            }

        }

        val filenameTI: TextInputLayout = findViewById(R.id.filenameTI)
        val imgFormatTI: TextInputLayout = findViewById(R.id.imgFormatTI)
        val imgFileSizeTI: TextInputLayout = findViewById(R.id.imgFileSizeTI)
        val imgWidthTI: TextInputLayout = findViewById(R.id.imgWidthTI)
        val imgHeightTI: TextInputLayout = findViewById(R.id.imgHeightTI)
        val imgDateTI: TextInputLayout = findViewById(R.id.imgDateTI)
        val imgDateDigitizedTI: TextInputLayout = findViewById(R.id.imgDateDigitizedTI)
        val imgLastModifiedDateTI: TextInputLayout = findViewById(R.id.imgLastModifiedDateTI)
        val gpsLatTI: TextInputLayout = findViewById(R.id.GPSLatTI)
        val gpsLongTI: TextInputLayout = findViewById(R.id.GPSLongTI)
        val gpsLocationTI: TextInputLayout = findViewById(R.id.gpsLocationTI)
        val camMakerTI: TextInputLayout = findViewById(R.id.camMakerTI)
        val camModelTI: TextInputLayout = findViewById(R.id.camModelTI)
        val exifLensMakerTI: TextInputLayout = findViewById(R.id.exifLensMakerTI)
        val exifLensModelTI: TextInputLayout = findViewById(R.id.exifLensModelTI)
        val focalLengthTI: TextInputLayout = findViewById(R.id.focalLengthTI)
        val camFlashTI: TextInputLayout = findViewById(R.id.camFlashTI)
        val imgBrightnessTI: TextInputLayout = findViewById(R.id.imgBrightnessTI)
        val whiteBalanceTI: TextInputLayout = findViewById(R.id.whiteBalanceTI)
        val colorSpaceTI: TextInputLayout = findViewById(R.id.colorSpaceTI)
        val imgOrientationTI: TextInputLayout = findViewById(R.id.imgOrientationTI)
        val imgXResTI: TextInputLayout = findViewById(R.id.imgXResTI)
        val imgYResTI: TextInputLayout = findViewById(R.id.imgYResTI)
        val imgResUnitTI: TextInputLayout = findViewById(R.id.imgResUnitTI)
        val imgYPositioningTI: TextInputLayout = findViewById(R.id.imgYPositioningTI)
        val imgArtistTI: TextInputLayout = findViewById(R.id.imgArtistTI)
        val imgCopyrightTI: TextInputLayout = findViewById(R.id.imgCopyrightTI)
        val imgSoftwareTI: TextInputLayout = findViewById(R.id.imgSoftwareTI)
        val exifFNumberTI: TextInputLayout = findViewById(R.id.exifFNumberTI)
        val exifISOSpeedTI: TextInputLayout = findViewById(R.id.exifISOSpeedTI)
        val exifExposureTimeTI: TextInputLayout = findViewById(R.id.exifExposureTimeTI)
        val exifExposureBiasValueTI: TextInputLayout = findViewById(R.id.exifExposureBiasValueTI)
        val exifExposureProgramTI: TextInputLayout = findViewById(R.id.exifExposureProgramTI)
        val exifApertureValueTI: TextInputLayout = findViewById(R.id.exifApertureValueTI)
        val exifMeteringModeTI: TextInputLayout = findViewById(R.id.exifMeteringModeTI)
        val sensitivityTypeTI: TextInputLayout = findViewById(R.id.sensitivityTypeTI)
        val sceneTypeTI: TextInputLayout = findViewById(R.id.sceneTypeTI)
        val sceneCaptureTypeTI: TextInputLayout = findViewById(R.id.sceneCaptureTypeTI)
        val sensingMethodTI: TextInputLayout = findViewById(R.id.sensingMethodTI)
        val exifVersionTI: TextInputLayout = findViewById(R.id.exifVersionTI)


        val theFileName: EditText = findViewById(R.id.theFileName)
        val imgFormat: EditText = findViewById(R.id.imgFormat)
        val imgFileSize: EditText = findViewById(R.id.imgFileSize)
        val imgWidth: EditText = findViewById(R.id.imgWidth)
        val imgHeight: EditText = findViewById(R.id.imgHeight)
        val imgDate: EditText = findViewById(R.id.imgDate)
        val imgDateDigitized: EditText = findViewById(R.id.imgDateDigitized)
        val imgLastModifiedDate: EditText = findViewById(R.id.imgLastModifiedDate)
        val gpsLat: EditText = findViewById(R.id.GPSLat)
        val gpsLong: EditText = findViewById(R.id.GPSLong)
        val gpsLocation: TextView = findViewById(R.id.gpsLocation)
        val camMaker: EditText = findViewById(R.id.camMaker)
        val camModel: EditText = findViewById(R.id.camModel)
        val exifLensMaker: EditText = findViewById(R.id.exifLensMaker)
        val exifLensModel: EditText = findViewById(R.id.exifLensModel)
        val focalLength: EditText = findViewById(R.id.focalLength)
        val camFlash: EditText = findViewById(R.id.camFlash)
        val imgBrightness: EditText = findViewById(R.id.imgBrightness)
        val whiteBalance: EditText = findViewById(R.id.whiteBalance)
        val colorSpace: EditText = findViewById(R.id.colorSpace)
        val imgOrientation: EditText = findViewById(R.id.imgOrientation)
        val imgXRes: EditText = findViewById(R.id.imgXRes)
        val imgYRes: EditText = findViewById(R.id.imgYRes)
        val imgResUnit: EditText = findViewById(R.id.imgResUnit)
        val imgYPositioning: EditText = findViewById(R.id.imgYPositioning)
        val imgArtist: EditText = findViewById(R.id.imgArtist)
        val imgCopyright: EditText = findViewById(R.id.imgCopyright)
        val imgSoftware: EditText = findViewById(R.id.imgSoftware)
        val exifFNumber: EditText = findViewById(R.id.exifFNumber)
        val exifISOSpeed: EditText = findViewById(R.id.exifISOSpeed)
        val exifExposureTime: EditText = findViewById(R.id.exifExposureTime)
        val exifExposureBiasValue: EditText = findViewById(R.id.exifExposureBiasValue)
        val exifExposureProgram: EditText = findViewById(R.id.exifExposureProgram)
        val exifApertureValue: EditText = findViewById(R.id.exifApertureValue)
        val exifMeteringMode: EditText = findViewById(R.id.exifMeteringMode)
        val sensitivityType: EditText = findViewById(R.id.sensitivityType)
        val sceneType: EditText = findViewById(R.id.sceneType)
        val sceneCaptureType: EditText = findViewById(R.id.sceneCaptureType)
        val sensingMethod: EditText = findViewById(R.id.sensingMethod)
        val exifVersion: EditText = findViewById(R.id.exifVersion)

        btnCopyAll = findViewById(R.id.btnCopyAll)
        btnCopyAll.setOnClickListener {
            var allTheData: String?

            if (theFileName.text.toString().isNotEmpty()) {
                allTheData = "File Name: " + theFileName.text.toString() + "\n"
                if (imgFormat.text.isNotEmpty()) {
                    allTheData = allTheData + "Image Format: " + imgFormat.text.toString() + "\n"
                }
                if (imgFileSize.text.isNotEmpty()) {
                    allTheData = allTheData + "Image File Size: " + imgFileSize.text.toString() + "\n"
                }
                if (imgWidth.text.isNotEmpty()) {
                    allTheData = allTheData + "Image Width: " + imgWidth.text.toString() + "\n"
                }
                if (imgHeight.text.isNotEmpty()) {
                    allTheData = allTheData + "Image Height: " + imgHeight.text.toString() + "\n"
                }
                if (imgDate.text.isNotEmpty()) {
                    allTheData = allTheData + "Original Date: " + imgDate.text.toString() + "\n"
                }
                if (imgDateDigitized.text.isNotEmpty()) {
                    allTheData = allTheData + "Digitized Date: " + imgDateDigitized.text.toString() + "\n"
                }
                if (imgLastModifiedDate.text.isNotEmpty()) {
                    allTheData = allTheData + "Last Modified Date: " + imgLastModifiedDate.text.toString() + "\n"
                }
                if (gpsLat.text.isNotEmpty()) {
                    allTheData = allTheData + "GPS Latitude: " + gpsLat.text.toString() + "\n"
                }
                if (gpsLong.text.isNotEmpty()) {
                    allTheData = allTheData + "GPS Longitude: " + gpsLong.text.toString() + "\n"
                }
                if (gpsLocation.text.isNotEmpty()) {
                    allTheData = allTheData + "Readable Address: " + gpsLocation.text.toString() + "\n"
                }
                if (camMaker.text.isNotEmpty()) {
                    allTheData = allTheData + "Camera Maker: " + camMaker.text.toString() + "\n"
                }
                if (camModel.text.isNotEmpty()) {
                    allTheData = allTheData + "Camera Model: " + camModel.text.toString() + "\n"
                }
                if (exifLensMaker.text.isNotEmpty()) {
                    allTheData = allTheData + "Lens Maker: " + exifLensMaker.text.toString() + "\n"
                }
                if (exifLensModel.text.isNotEmpty()) {
                    allTheData = allTheData + "Lens Model: " + exifLensModel.text.toString() + "\n"
                }
                if (focalLength.text.isNotEmpty()) {
                    allTheData = allTheData + "Focal Length: " + focalLength.text.toString() + "\n"
                }
                if (camFlash.text.isNotEmpty()) {
                    allTheData = allTheData + "Flash: " + camFlash.text.toString() + "\n"
                }
                if (imgBrightness.text.isNotEmpty()) {
                    allTheData = allTheData + "Brightness: " + imgBrightness.text.toString() + "\n"
                }
                if (whiteBalance.text.isNotEmpty()) {
                    allTheData = allTheData + "White Balance: " + whiteBalance.text.toString() + "\n"
                }
                if (colorSpace.text.isNotEmpty()) {
                    allTheData = allTheData + "Color Space: " + colorSpace.text.toString() + "\n"
                }
                if (imgOrientation.text.isNotEmpty()) {
                    allTheData = allTheData + "Image Orientation: " + imgOrientation.text.toString() + "\n"
                }
                if (imgXRes.text.isNotEmpty()) {
                    allTheData = allTheData + "X Resolution: " + imgXRes.text.toString() + "\n"
                }
                if (imgYRes.text.isNotEmpty()) {
                    allTheData = allTheData + "Y Resolution: " + imgYRes.text.toString() + "\n"
                }
                if (imgResUnit.text.isNotEmpty()) {
                    allTheData = allTheData + "Resolution Unit: " + imgResUnit.text.toString() + "\n"
                }
                if (imgYPositioning.text.isNotEmpty()) {
                    allTheData = allTheData + "YCbCrPositioning: " + imgYPositioning.text.toString() + "\n"
                }
                if (imgArtist.text.isNotEmpty()) {
                    allTheData = allTheData + "Image Artist: " + imgArtist.text.toString() + "\n"
                }
                if (imgCopyright.text.isNotEmpty()) {
                    allTheData = allTheData + "Copyright: " + imgCopyright.text.toString() + "\n"
                }
                if (imgSoftware.text.isNotEmpty()) {
                    allTheData = allTheData + "Software: " + imgSoftware.text.toString() + "\n"
                }
                if (exifFNumber.text.isNotEmpty()) {
                    allTheData = allTheData + "F-Stop (F-Number): " + exifFNumber.text.toString() + "\n"
                }
                if (exifISOSpeed.text.isNotEmpty()) {
                    allTheData = allTheData + "ISO: " + exifISOSpeed.text.toString() + "\n"
                }
                if (exifExposureTime.text.isNotEmpty()) {
                    allTheData = allTheData + "Shutter Speed: " + exifExposureTime.text.toString() + "\n"
                }
                if (exifExposureBiasValue.text.isNotEmpty()) {
                    allTheData = allTheData + "Exposure Bias: " + exifExposureBiasValue.text.toString() + "\n"
                }
                if (exifExposureProgram.text.isNotEmpty()) {
                    allTheData = allTheData + "Exposure Program: " + exifExposureProgram.text.toString() + "\n"
                }
                if (exifApertureValue.text.isNotEmpty()) {
                    allTheData = allTheData + "Aperture: " + exifApertureValue.text.toString() + "\n"
                }
                if (exifMeteringMode.text.isNotEmpty()) {
                    allTheData = allTheData + "Metering Mode: " + exifMeteringMode.text.toString() + "\n"
                }
                if (sensitivityType.text.isNotEmpty()) {
                    allTheData = allTheData + "Sensitivity Type: " + sensitivityType.text.toString() + "\n"
                }
                if (sceneType.text.isNotEmpty()) {
                    allTheData = allTheData + "Scene Type: " + sceneType.text.toString() + "\n"
                }
                if (sceneCaptureType.text.isNotEmpty()) {
                    allTheData = allTheData + "Scene Capture Type: " + sceneCaptureType.text.toString() + "\n"
                }
                if (sensingMethod.text.isNotEmpty()) {
                    allTheData = allTheData + "Sensing Method: " + sensingMethod.text.toString() + "\n"
                }
                if (exifVersion.text.isNotEmpty()) {
                    allTheData = allTheData + "Exif Version: " + exifVersion.text.toString() + "\n"
                }

                allTheData = "$allTheData\nGenerated by Exif Viewer\nversion: $versionName\nwww.AminBeheshti.com"
                copy2Clipboard(allTheData)
                Toast.makeText(this, "Copied to clipboard", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "No Data to Copy!", Toast.LENGTH_SHORT).show()
            }
        }


        filenameTI.setEndIconOnClickListener {
            val theLabel = "File Name: "
            validateText(theLabel, theFileName.text.toString())
        }

        imgFormatTI.setEndIconOnClickListener {
            val theLabel = "Image Format: "
            validateText(theLabel, imgFormat.text.toString())
        }

        imgFileSizeTI.setEndIconOnClickListener {
            val theLabel = "Image File Size: "
            validateText(theLabel, imgFileSize.text.toString())
        }

        imgWidthTI.setEndIconOnClickListener {
            val theLabel = "Image Width: "
            validateText(theLabel, imgWidth.text.toString())
        }

        imgHeightTI.setEndIconOnClickListener {
            val theLabel = "Image Height: "
            validateText(theLabel, imgHeight.text.toString())
        }

        imgDateTI.setEndIconOnClickListener {
            val theLabel = "Original Date: "
            validateText(theLabel, imgDate.text.toString())
        }

        imgDateDigitizedTI.setEndIconOnClickListener {
            val theLabel = "Digitized Date: "
            validateText(theLabel, imgDateDigitized.text.toString())
        }

        imgLastModifiedDateTI.setEndIconOnClickListener {
            val theLabel = "Last Modified Date: "
            validateText(theLabel, imgLastModifiedDate.text.toString())
        }

        gpsLatTI.setEndIconOnClickListener {
            val theLabel = "GPS Latitude: "
            validateText(theLabel, gpsLat.text.toString())
        }

        gpsLongTI.setEndIconOnClickListener {
            val theLabel = "GPS Longitude: "
            validateText(theLabel, gpsLong.text.toString())
        }

        gpsLocationTI.setEndIconOnClickListener {
            val theLabel = ""
            validateText(theLabel, gpsLocation.text.toString())
        }

        camMakerTI.setEndIconOnClickListener {
            val theLabel = "Camera Maker: "
            validateText(theLabel, camMaker.text.toString())
        }

        camModelTI.setEndIconOnClickListener {
            val theLabel = "Camera Model: "
            validateText(theLabel, camModel.text.toString())
        }

        exifLensMakerTI.setEndIconOnClickListener {
            val theLabel = "Lens Maker: "
            validateText(theLabel, exifLensMaker.text.toString())
        }

        exifLensModelTI.setEndIconOnClickListener {
            val theLabel = "Lens Model: "
            validateText(theLabel, exifLensModel.text.toString())
        }

        focalLengthTI.setEndIconOnClickListener {
            val theLabel = "Focal Length: "
            validateText(theLabel, focalLength.text.toString())
        }

        camFlashTI.setEndIconOnClickListener {
            val theLabel = "Flash: "
            validateText(theLabel, camFlash.text.toString())
        }

        imgBrightnessTI.setEndIconOnClickListener {
            val theLabel = "Brightness: "
            validateText(theLabel, imgBrightness.text.toString())
        }

        whiteBalanceTI.setEndIconOnClickListener {
            val theLabel = "White Balance: "
            validateText(theLabel, whiteBalance.text.toString())
        }

        colorSpaceTI.setEndIconOnClickListener {
            val theLabel = "Color Space: "
            validateText(theLabel, colorSpace.text.toString())
        }

        imgOrientationTI.setEndIconOnClickListener {
            val theLabel = "Image Orientation: "
            validateText(theLabel, imgOrientation.text.toString())
        }

        imgXResTI.setEndIconOnClickListener {
            val theLabel = "X Resolution: "
            validateText(theLabel, imgXRes.text.toString())
        }

        imgYResTI.setEndIconOnClickListener {
            val theLabel = "Y Resolution: "
            validateText(theLabel, imgYRes.text.toString())
        }

        imgResUnitTI.setEndIconOnClickListener {
            val theLabel = "Resolution Unit: "
            validateText(theLabel, imgResUnit.text.toString())
        }

        imgYPositioningTI.setEndIconOnClickListener {
            val theLabel = "YCbCrPositioning: "
            validateText(theLabel, imgYPositioning.text.toString())
        }

        imgArtistTI.setEndIconOnClickListener {
            val theLabel = "Image Artist: "
            validateText(theLabel, imgArtist.text.toString())
        }

        imgCopyrightTI.setEndIconOnClickListener {
            val theLabel = "Copyright: "
            validateText(theLabel, imgCopyright.text.toString())
        }

        imgSoftwareTI.setEndIconOnClickListener {
            val theLabel = "Software: "
            validateText(theLabel, imgSoftware.text.toString())
        }

        exifFNumberTI.setEndIconOnClickListener {
            val theLabel = "F-Stop (F-Number): "
            validateText(theLabel, exifFNumber.text.toString())
        }

        exifISOSpeedTI.setEndIconOnClickListener {
            val theLabel = "ISO: "
            validateText(theLabel, exifISOSpeed.text.toString())
        }

        exifExposureTimeTI.setEndIconOnClickListener {
            val theLabel = "Shutter Speed: "
            validateText(theLabel, exifExposureTime.text.toString())
        }

        exifExposureBiasValueTI.setEndIconOnClickListener {
            val theLabel = "Exposure Bias: "
            validateText(theLabel, exifExposureBiasValue.text.toString())
        }

        exifExposureProgramTI.setEndIconOnClickListener {
            val theLabel = "Exposure Program: "
            validateText(theLabel, exifExposureProgram.text.toString())
        }

        exifApertureValueTI.setEndIconOnClickListener {
            val theLabel = "Aperture: "
            validateText(theLabel, exifApertureValue.text.toString())
        }

        exifMeteringModeTI.setEndIconOnClickListener {
            val theLabel = "Metering Mode: "
            validateText(theLabel, exifMeteringMode.text.toString())
        }

        sensitivityTypeTI.setEndIconOnClickListener {
            val theLabel = "Sensitivity Type: "
            validateText(theLabel, sensitivityType.text.toString())
        }

        sceneTypeTI.setEndIconOnClickListener {
            val theLabel = "Scene Type: "
            validateText(theLabel, sceneType.text.toString())
        }

        sceneCaptureTypeTI.setEndIconOnClickListener {
            val theLabel = "Scene Capture Type: "
            validateText(theLabel, sceneCaptureType.text.toString())
        }

        sensingMethodTI.setEndIconOnClickListener {
            val theLabel = "Sensing Method: "
            validateText(theLabel, sensingMethod.text.toString())
        }

        exifVersionTI.setEndIconOnClickListener {
            val theLabel = "Exif Version: "
            validateText(theLabel, exifVersion.text.toString())
        }

    }

    override fun onRequestPermissionsResult(
            requestCode: Int,
            permissions: Array<out String>,
            grantResults: IntArray
    ) {
        if (requestCode == READ_EXTERNAL_PHOTOS_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                launchIntentForPhotos()
            } else {
                Toast.makeText(
                        this,
                        "In order to pick an image from your gallery, you need to provide access to your phone",
                        Toast.LENGTH_LONG
                ).show()
            }
        }

        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
    }

    @SuppressLint("SetTextI18n")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == RESULT_OK && requestCode == PICK_PHOTO_CODE) {
            imageUri = data?.data

            val filenameTI: TextInputLayout = findViewById(R.id.filenameTI)
            val imgFormatTI: TextInputLayout = findViewById(R.id.imgFormatTI)
            val imgFileSizeTI: TextInputLayout = findViewById(R.id.imgFileSizeTI)

            val imageFilename: EditText = findViewById(R.id.theFileName)
            val imageFormat: EditText = findViewById(R.id.imgFormat)
            val imageFileSize: EditText = findViewById(R.id.imgFileSize)
            imageFileSize.text = null
            imageFormat.text = null
            imageFilename.text = null
            val imgFormat = imageUri?.let { contentResolver.getType(it) }
            imageFormat.setText(imgFormat)
            imgFormatTI.setEndIconDrawable(R.drawable.ic_content_copy)

            val cursorSec: Cursor? = imageUri?.let { contentResolver.query(it, null, null, null, null) }

            if (cursorSec == null) {
                var theFilePath = imageUri?.path
            } else {
                val nameIndex = cursorSec.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                val sizeIndex = cursorSec.getColumnIndex(OpenableColumns.SIZE)
                cursorSec.moveToFirst()
                val pictureFileName = nameIndex.let { cursorSec.getString(it) }
                val pictureSize = sizeIndex.let { cursorSec.getLong(it).toString() }
                cursorSec.close()

                imageFilename.setText(pictureFileName)
                filenameTI.setEndIconDrawable(R.drawable.ic_content_copy)

                val sizeInMb = pictureSize.toLong() / (1024.0 * 1024)
                val sizeInMbStr = "%.2f".format(sizeInMb)
                imageFileSize.setText("$sizeInMbStr MB")
                imgFileSizeTI.setEndIconDrawable(R.drawable.ic_content_copy)
                Log.d(TAG, "Size=${sizeInMbStr}MB")
            }

            imageView.setImageResource(0)
            imageView.setImageURI(imageUri)

            showExif(imageUri)
        }
    }

    @SuppressLint("SetTextI18n")
    private fun showExif(imageUri: Uri?) {
        val latitude: Float
        val longitude: Float

        val inputStream = imageUri?.let { contentResolver.openInputStream(it) }
        val exifInterface = inputStream?.let { ExifInterface(it) }
        // Now you can extract any Exif tag you want
        // Assuming the image is a JPEG or supported raw format
        val imgWidthExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_IMAGE_WIDTH)
        val imgHeightExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_IMAGE_LENGTH)
        val imgDateExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_DATETIME_ORIGINAL)
        val imgDateDigitizedExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_DATETIME_DIGITIZED)
        val imgLastModifiedDateExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_DATETIME)
        val cameraMakerExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_MAKE)
        val cameraModelExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_MODEL)
        val latGPSExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_GPS_LATITUDE)
        val longGPSExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_GPS_LONGITUDE)
        val latRefExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_GPS_LATITUDE_REF)
        val longRefExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_GPS_LONGITUDE_REF)
        val imgOrientationExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_ORIENTATION)
        val imgBrightnessExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_BRIGHTNESS_VALUE)
        val imgWhiteBalanceExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_WHITE_BALANCE)
        val colorSpaceExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_COLOR_SPACE)
        val focalLengthExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_FOCAL_LENGTH)
        val flashExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_FLASH)
        val softwareExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_SOFTWARE)
        val imgXResExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_X_RESOLUTION)
        val imgYResExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_Y_RESOLUTION)
        val imgResUnitExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_RESOLUTION_UNIT)
        val imgYPositioningExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_Y_CB_CR_POSITIONING)
        val imgArtistExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_ARTIST)
        val imgCopyrightExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_COPYRIGHT)
        val lensMakerExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_LENS_MAKE)
        val lensModelExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_LENS_MODEL)
        val fNumberExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_F_NUMBER)
        val isoSpeedExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_PHOTOGRAPHIC_SENSITIVITY)
        val exposureTimeExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_EXPOSURE_TIME)
        val exposureBiasValueExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_EXPOSURE_BIAS_VALUE)
        val exposureProgramExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_EXPOSURE_PROGRAM)
        val apertureValueExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_APERTURE_VALUE)
        val meteringModeExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_METERING_MODE)
        val sensitivityTypeExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_SENSITIVITY_TYPE)
        val sceneTypeExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_SCENE_TYPE)
        val sceneCaptureTypeExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_SCENE_CAPTURE_TYPE)
        val sensingMethodExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_SENSING_METHOD)
        val eVersionExif: String? = exifInterface?.getAttribute(ExifInterface.TAG_EXIF_VERSION)

        val imageWidth: EditText = findViewById(R.id.imgWidth)
        val imageHeight: EditText = findViewById(R.id.imgHeight)
        val imageDate: EditText = findViewById(R.id.imgDate)
        val imageDateDigitized: EditText = findViewById(R.id.imgDateDigitized)
        val imageLastModifiedDate: EditText = findViewById(R.id.imgLastModifiedDate)
        val cameraMaker: EditText = findViewById(R.id.camMaker)
        val cameraModel: EditText = findViewById(R.id.camModel)
        val latGPS: EditText = findViewById(R.id.GPSLat)
        val longGPS: EditText = findViewById(R.id.GPSLong)
        val readableAddress: TextView = findViewById(R.id.gpsLocation)
        val imgOrientation: EditText = findViewById(R.id.imgOrientation)
        val imgBrightness: EditText = findViewById(R.id.imgBrightness)
        val imgWhiteBalance: EditText = findViewById(R.id.whiteBalance)
        val colorSpace: EditText = findViewById(R.id.colorSpace)
        val focalLength: EditText = findViewById(R.id.focalLength)
        val flash: EditText = findViewById(R.id.camFlash)
        val software: EditText = findViewById(R.id.imgSoftware)
        val imgXRes: EditText = findViewById(R.id.imgXRes)
        val imgYRes: EditText = findViewById(R.id.imgYRes)
        val imgResUnit: EditText = findViewById(R.id.imgResUnit)
        val imgYPositioning: EditText = findViewById(R.id.imgYPositioning)
        val imgArtist: EditText = findViewById(R.id.imgArtist)
        val imgCopyright: EditText = findViewById(R.id.imgCopyright)
        val lensMaker: EditText = findViewById(R.id.exifLensMaker)
        val lensModel: EditText = findViewById(R.id.exifLensModel)
        val fNumber: EditText = findViewById(R.id.exifFNumber)
        val isoSpeed: EditText = findViewById(R.id.exifISOSpeed)
        val exposureTime: EditText = findViewById(R.id.exifExposureTime)
        val exposureBiasValue: EditText = findViewById(R.id.exifExposureBiasValue)
        val exposureProgram: EditText = findViewById(R.id.exifExposureProgram)
        val apertureValue: EditText = findViewById(R.id.exifApertureValue)
        val meteringMode: EditText = findViewById(R.id.exifMeteringMode)
        val sensitivityType: EditText = findViewById(R.id.sensitivityType)
        val sceneType: EditText = findViewById(R.id.sceneType)
        val sceneCaptureType: EditText = findViewById(R.id.sceneCaptureType)
        val sensingMethod: EditText = findViewById(R.id.sensingMethod)
        val exifVersion: EditText = findViewById(R.id.exifVersion)

        imageWidth.text = null
        imageHeight.text = null
        imageDate.text = null
        cameraMaker.text = null
        cameraModel.text = null
        latGPS.text = null
        longGPS.text = null
        readableAddress.text = null
        imgOrientation.text = null
        imgBrightness.text = null
        imgWhiteBalance.text = null
        colorSpace.text = null
        focalLength.text = null
        flash.text = null
        software.text = null
        imgXRes.text = null
        imgYRes.text = null
        imgResUnit.text = null
        imgYPositioning.text = null
        imgArtist.text = null
        imgCopyright.text = null
        lensMaker.text = null
        lensModel.text = null
        fNumber.text = null
        isoSpeed.text = null
        exposureTime.text = null
        exposureBiasValue.text = null
        exposureProgram.text = null
        apertureValue.text = null
        meteringMode.text = null
        sensitivityType.text = null
        sceneType.text = null
        sceneCaptureType.text = null
        sensingMethod.text = null
        imageDateDigitized.text = null
        imageLastModifiedDate.text = null
        exifVersion.text = null

        // ---------------------------------------------------------------------------------------
        val imgWidthTI: TextInputLayout = findViewById(R.id.imgWidthTI)
        val imgHeightTI: TextInputLayout = findViewById(R.id.imgHeightTI)
        val imgDateTI: TextInputLayout = findViewById(R.id.imgDateTI)
        val imgDateDigitizedTI: TextInputLayout = findViewById(R.id.imgDateDigitizedTI)
        val imgLastModifiedDateTI: TextInputLayout = findViewById(R.id.imgLastModifiedDateTI)
        val gpsLatTI: TextInputLayout = findViewById(R.id.GPSLatTI)
        val gpsLongTI: TextInputLayout = findViewById(R.id.GPSLongTI)
        val camMakerTI: TextInputLayout = findViewById(R.id.camMakerTI)
        val camModelTI: TextInputLayout = findViewById(R.id.camModelTI)
        val exifLensMakerTI: TextInputLayout = findViewById(R.id.exifLensMakerTI)
        val exifLensModelTI: TextInputLayout = findViewById(R.id.exifLensModelTI)
        val focalLengthTI: TextInputLayout = findViewById(R.id.focalLengthTI)
        val camFlashTI: TextInputLayout = findViewById(R.id.camFlashTI)
        val imgBrightnessTI: TextInputLayout = findViewById(R.id.imgBrightnessTI)
        val whiteBalanceTI: TextInputLayout = findViewById(R.id.whiteBalanceTI)
        val colorSpaceTI: TextInputLayout = findViewById(R.id.colorSpaceTI)
        val imgOrientationTI: TextInputLayout = findViewById(R.id.imgOrientationTI)
        val imgXResTI: TextInputLayout = findViewById(R.id.imgXResTI)
        val imgYResTI: TextInputLayout = findViewById(R.id.imgYResTI)
        val imgResUnitTI: TextInputLayout = findViewById(R.id.imgResUnitTI)
        val imgYPositioningTI: TextInputLayout = findViewById(R.id.imgYPositioningTI)
        val imgArtistTI: TextInputLayout = findViewById(R.id.imgArtistTI)
        val imgCopyrightTI: TextInputLayout = findViewById(R.id.imgCopyrightTI)
        val imgSoftwareTI: TextInputLayout = findViewById(R.id.imgSoftwareTI)
        val exifFNumberTI: TextInputLayout = findViewById(R.id.exifFNumberTI)
        val exifISOSpeedTI: TextInputLayout = findViewById(R.id.exifISOSpeedTI)
        val exifExposureTimeTI: TextInputLayout = findViewById(R.id.exifExposureTimeTI)
        val exifExposureBiasValueTI: TextInputLayout = findViewById(R.id.exifExposureBiasValueTI)
        val exifExposureProgramTI: TextInputLayout = findViewById(R.id.exifExposureProgramTI)
        val exifApertureValueTI: TextInputLayout = findViewById(R.id.exifApertureValueTI)
        val exifMeteringModeTI: TextInputLayout = findViewById(R.id.exifMeteringModeTI)
        val sensitivityTypeTI: TextInputLayout = findViewById(R.id.sensitivityTypeTI)
        val sceneTypeTI: TextInputLayout = findViewById(R.id.sceneTypeTI)
        val sceneCaptureTypeTI: TextInputLayout = findViewById(R.id.sceneCaptureTypeTI)
        val sensingMethodTI: TextInputLayout = findViewById(R.id.sensingMethodTI)
        val exifVersionTI: TextInputLayout = findViewById(R.id.exifVersionTI)
        // ---------------------------------------------------------------------------------------

        if (imgWidthExif != null) {
            if (imgWidthExif.isNotEmpty()) {
                imageWidth.setText("$imgWidthExif pixels")
                imgWidthTI.setEndIconDrawable(R.drawable.ic_content_copy)
            }
        }
        if (imgHeightExif != null) {
            imageHeight.setText("$imgHeightExif pixels")
            imgHeightTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (imgDateExif != null) {
            imageDate.setText(imgDateExif)
            imgDateTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgDateDigitizedExif != null) {
            imageDateDigitized.setText(imgDateDigitizedExif)
            imgDateDigitizedTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgLastModifiedDateExif != null) {
            imageLastModifiedDate.setText(imgLastModifiedDateExif)
            imgLastModifiedDateTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (cameraMakerExif != null) {
            cameraMaker.setText(cameraMakerExif)
            camMakerTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (cameraModelExif != null) {
            cameraModel.setText(cameraModelExif)
            camModelTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if ((latGPSExif != null)
                && (latRefExif != null)
                && (longGPSExif != null)
                && (longRefExif != null)) {

            latitude = if (latRefExif == "N") {
                convertToDegree(latGPSExif)
            } else {
                0 - convertToDegree(latGPSExif)
            }

            longitude = if (longRefExif == "E") {
                convertToDegree(longGPSExif)
            } else {
                0 - convertToDegree(longGPSExif)
            }

            latGPS.setText("$latitude")
            longGPS.setText("$longitude")
            gpsLatTI.setEndIconDrawable(R.drawable.ic_content_copy)
            gpsLongTI.setEndIconDrawable(R.drawable.ic_content_copy)

        }

        if (imgOrientationExif != null) {

            val imgOrientationTranslated: String = when (imgOrientationExif) {
                "0" -> "UNDEFINED"
                "1" -> "Horizontal (normal)"
                "2" -> "Mirror horizontal"
                "3" -> "Rotate 180"
                "4" -> "Mirror vertical"
                "5" -> "Mirror horizontal and rotate 270 CW"
                "6" -> "Rotate 90 CW"
                "7" -> "Mirror horizontal and rotate 90 CW"
                "8" -> "Rotate 270 CW"
                else -> { // Note the block
                    imgOrientationExif
                }
            }
            imgOrientation.setText(imgOrientationTranslated)
            imgOrientationTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgBrightnessExif != null) {
            imgBrightness.setText(imgBrightnessExif)
            imgBrightnessTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgWhiteBalanceExif != null) {

            val whiteBalanceTranslated: String = when (imgWhiteBalanceExif) {
                "0" -> "Auto white balance"
                "1" -> "Manual white balance"
                else -> { // Note the block
                    imgWhiteBalanceExif
                }
            }
            imgWhiteBalance.setText(whiteBalanceTranslated)
            whiteBalanceTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (colorSpaceExif != null) {
            val colorSpaceConvert: String?
            val hexString: String = Integer.toHexString(colorSpaceExif.toInt())

            colorSpaceConvert = when (hexString.lowercase(Locale.ROOT)) {
                "1" -> "sRGB"
                "2" -> "Adobe RGB"
                "fffd" -> "Wide Gamut RGB"
                "fffe" -> "ICC Profile"
                "ffff" -> "Uncalibrated"
                else -> { // Note the block
                    colorSpaceExif
                }
            }
            colorSpace.setText(colorSpaceConvert)
            colorSpaceTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (focalLengthExif != null) {
            focalLength.setText(focalLengthExif)
            focalLengthTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (flashExif != null) {
            val flashConvert: String?
            val hexString: String = Integer.toHexString(flashExif.toInt())

            when (hexString.lowercase(Locale.ROOT)) {
                "00" -> flashConvert = "Flash did not fire"
                "01" -> flashConvert = "Flash fired"
                "05" -> flashConvert = "Strobe return light not detected"
                "07" -> flashConvert = "Strobe return light detected"
                "08" -> flashConvert = "On, Did not fire"
                "09" -> flashConvert = "Flash fired, compulsory flash mode"
                "0d" -> flashConvert = "Flash fired, compulsory flash mode, return light not detected"
                "0f" -> flashConvert = "Flash fired, compulsory flash mode, return light detected"
                "10" -> flashConvert = "Flash did not fire, compulsory flash mode"
                "14" -> flashConvert = "Off, Did not fire, Return not detected"
                "18" -> flashConvert = "Flash did not fire, auto mode"
                "19" -> flashConvert = "Flash fired, auto mode"
                "1d" -> flashConvert = "Flash fired, auto mode, return light not detected"
                "1f" -> flashConvert = "Flash fired, auto mode, return light detected"
                "20" -> flashConvert = "No flash function"
                "30" -> flashConvert = "Off, No flash function"
                "41" -> flashConvert = "Flash fired, red-eye reduction mode"
                "45" -> flashConvert = "Flash fired, red-eye reduction mode, return light not detected"
                "47" -> flashConvert = "Flash fired, red-eye reduction mode, return light detected"
                "49" -> flashConvert = "Flash fired, compulsory flash mode, red-eye reduction mode"
                "4d" -> flashConvert = "Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected"
                "4f" -> flashConvert = "Flash fired, compulsory flash mode, red-eye reduction mode, return light detected"
                "50" -> flashConvert = "Off, Red-eye reduction"
                "58" -> flashConvert = "Auto, Did not fire, Red-eye reduction"
                "59" -> flashConvert = "Flash fired, auto mode, red-eye reduction mode"
                "5d" -> flashConvert = "Flash fired, auto mode, return light not detected, red-eye reduction mode"
                "5f" -> flashConvert = "Flash fired, auto mode, return light detected, red-eye reduction mode"
                else -> { // Note the block
                    flashConvert = flashExif
                }
            }

            flash.setText(flashConvert)
            camFlashTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (softwareExif != null) {
            software.setText(softwareExif)
            imgSoftwareTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgXResExif != null) {
            imgXRes.setText(imgXResExif)
            imgXResTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgYResExif != null) {
            imgYRes.setText(imgYResExif)
            imgYResTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgResUnitExif != null) {

            val imgResUnitTranslated: String = when (imgResUnitExif) {
                "1" -> "No absolute unit of measurement."
                "2" -> "Inch"
                "3" -> "Centimeter"
                else -> { // Note the block
                    imgResUnitExif
                }
            }
            imgResUnit.setText(imgResUnitTranslated)
            imgResUnitTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgYPositioningExif != null) {

            val imgYPositioningTranslated: String = when (imgYPositioningExif) {
                "1" -> "Centered"
                "2" -> "Co-Sited"
                else -> { // Note the block
                    imgYPositioningExif
                }
            }
            imgYPositioning.setText(imgYPositioningTranslated)
            imgYPositioningTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgArtistExif != null) {
            imgArtist.setText(imgArtistExif)
            imgArtistTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (imgCopyrightExif != null) {
            imgCopyright.setText(imgCopyrightExif)
            imgCopyrightTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (lensMakerExif != null) {
            lensMaker.setText(lensMakerExif)
            exifLensMakerTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (lensModelExif != null) {
            lensModel.setText(lensModelExif)
            exifLensModelTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (fNumberExif != null) {
            fNumber.setText(fNumberExif)
            exifFNumberTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (isoSpeedExif != null) {
            isoSpeed.setText(isoSpeedExif)
            exifISOSpeedTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (exposureTimeExif != null) {
            exposureTime.setText("$exposureTimeExif seconds")
            exifExposureTimeTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (exposureBiasValueExif != null) {
            exposureBiasValue.setText(exposureBiasValueExif)
            exifExposureBiasValueTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (exposureProgramExif != null) {

            val exposureProgramTranslated: String = when (exposureProgramExif) {
                "0" -> "Not defined"
                "1" -> "Manual"
                "2" -> "Normal program"
                "3" -> "Aperture priority"
                "4" -> "Shutter priority"
                "5" -> "Creative program (biased toward depth of field)"
                "6" -> "Action program (biased toward fast shutter speed)"
                "7" -> "Portrait mode (for closeup photos with the background out of focus)"
                "8" -> "Landscape mode (for landscape photos with the background in focus)"
                "9" -> "Bulb"
                else -> { // Note the block
                    exposureProgramExif
                }
            }
            exposureProgram.setText(exposureProgramTranslated)
            exifExposureProgramTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (apertureValueExif != null) {
            apertureValue.setText(apertureValueExif)
            exifApertureValueTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }
        if (meteringModeExif != null) {

            val meteringModeTranslated: String = when (meteringModeExif) {
                "0" -> "Unknown"
                "1" -> "Average"
                "2" -> "Center Weighted Average"
                "3" -> "Spot"
                "4" -> "MultiSpot"
                "5" -> "Pattern"
                "6" -> "Partial"
                "255" -> "other"
                else -> { // Note the block
                    meteringModeExif
                }
            }
            meteringMode.setText(meteringModeTranslated)
            exifMeteringModeTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (sensitivityTypeExif != null) {

            val sensitivityTypeTranslated: String = when (sensitivityTypeExif) {
                "0" -> "Unknown"
                "1" -> "Standard Output Sensitivity"
                "2" -> "Recommended Exposure Index"
                "3" -> "ISO Speed"
                "4" -> "Standard Output Sensitivity and Recommended Exposure Index"
                "5" -> "Standard Output Sensitivity and ISO Speed"
                "6" -> "Recommended Exposure Index and ISO Speed"
                "7" -> "Standard Output Sensitivity, Recommended Exposure Index and ISO Speed"
                else -> { // Note the block
                    sensitivityTypeExif
                }
            }
            sensitivityType.setText(sensitivityTypeTranslated)
            sensitivityTypeTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (sceneTypeExif != null) {

            val sceneTypeTranslated: String = when (sceneTypeExif) {
                "1" -> "Directly photographed"
                else -> { // Note the block
                    sceneTypeExif
                }
            }
            sceneType.setText(sceneTypeTranslated)
            sceneTypeTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (sceneCaptureTypeExif != null) {

            val sceneCaptureTypeTranslated: String = when (sceneCaptureTypeExif) {
                "0" -> "Standard"
                "1" -> "Landscape"
                "2" -> "Portrait"
                "3" -> "Night"
                "4" -> "Other"
                else -> { // Note the block
                    sceneCaptureTypeExif
                }
            }
            sceneCaptureType.setText(sceneCaptureTypeTranslated)
            sceneCaptureTypeTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (sensingMethodExif != null) {

            val sensingMethodTranslated: String = when (sensingMethodExif) {
                "1" -> "Not defined"
                "2" -> "One-chip color area"
                "3" -> "Two-chip color area"
                "4" -> "Three-chip color area"
                "5" -> "Color sequential area"
                "6" -> "Tri-linear"
                "7" -> "Color sequential linear"
                else -> { // Note the block
                    sensingMethodExif
                }
            }
            sensingMethod.setText(sensingMethodTranslated)
            sensingMethodTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

        if (eVersionExif != null) {
            exifVersion.setText(eVersionExif)
            exifVersionTI.setEndIconDrawable(R.drawable.ic_content_copy)
        }

    }

    private fun launchIntentForPhotos() {
        val gallery = Intent(Intent.ACTION_GET_CONTENT, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
        gallery.type = "image/*"
        startActivityForResult(Intent.createChooser(gallery, "Choose an image"), PICK_PHOTO_CODE)
    }

    private fun validateText(theLabel: String, theText: String) {
        val theCompleteText: String = theLabel + theText
        if (theText.isNotEmpty()) {
            copy2Clipboard(theCompleteText)
            Toast.makeText(this, "Copied to Clipboard", Toast.LENGTH_SHORT).show()
        } else Toast.makeText(this, "No Text to Copy!", Toast.LENGTH_SHORT).show()
    }

    private fun copy2Clipboard(text: CharSequence) {
        val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
        val clip = ClipData.newPlainText("copy text", text)
        clipboard.setPrimaryClip(clip)
    }

    fun openLocationOnMap(view: View) {
        val lat: EditText = findViewById(R.id.GPSLat)
        val long: EditText = findViewById(R.id.GPSLong)
        val gpsLat: String = lat.text.toString()
        val gpsLong: String = long.text.toString()

        if (gpsLat.isNotEmpty() && gpsLong.isNotEmpty()) {
            val url = "https://www.google.com/maps?q=$gpsLat,$gpsLong"
            val intent = Intent(Intent.ACTION_VIEW)
            intent.data = Uri.parse(url)
            startActivity(intent)
        } else Toast.makeText(
                this,
                "The coordinate fields are empty or something went wrong!",
                Toast.LENGTH_SHORT
        ).show()
    }

    @SuppressLint("SetTextI18n")
    fun convertToReadableAddress(v: View) {

        val lat: EditText = findViewById(R.id.GPSLat)
        val long: EditText = findViewById(R.id.GPSLong)

        if (lat.text.isNotEmpty() && long.text.isNotEmpty()) {
            val gpsLat: String = (lat.text.toString())
            val gpsLong: String = (long.text.toString())

            if (gpsLat.isNotEmpty() && gpsLong.isNotEmpty()) {
                conToAddressAPI(gpsLat.toDouble(), gpsLong.toDouble())
            }
        } else Toast.makeText(this, "No data to convert!", Toast.LENGTH_SHORT).show()
    }

    private fun conToAddressAPI(lat: Double, long: Double) {
        val readableAddress: TextView = findViewById(R.id.gpsLocation)
        val gpsLocationTI: TextInputLayout = findViewById(R.id.gpsLocationTI)
        var address: String? = null
        var theContinent: String?
        var theCountryCode: String?
        var thePrincipalSubdivision: String?
        var theCity: String?
        var theLocality: String?
        var thePostalCode: String?

        // Instantiate the cache
        val cache = DiskBasedCache(cacheDir, 1024 * 1024) // 1MB cap

        // Set up the network to use HttpURLConnection as the HTTP client.
        val network = BasicNetwork(HurlStack())

        // Instantiate the RequestQueue with the cache and network. Start the queue.
        val requestQueue = RequestQueue(cache, network).apply {
            start()
        }
        val url = "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=$lat&longitude=$long&localityLanguage=en"

        val jsonObjectRequest = JsonObjectRequest(Request.Method.GET, url, null, { response ->

            theContinent = format(response.getString("continent"))
            theCountryCode = format(response.getString("countryName"))
            thePrincipalSubdivision = format(response.getString("principalSubdivision"))
            theCity = format(response.getString("city"))
            theLocality = format(response.getString("locality"))
            thePostalCode = format(response.getString("postcode"))

            if (thePostalCode != null) {
                if (thePostalCode!!.isNotEmpty()) {
                    address = "$thePostalCode"
                }
            }
            if (theLocality != null) {
                if (theLocality!!.isNotEmpty()) {
                    address = if (address != null) {
                        "$address, $theLocality"
                    } else {
                        "$theLocality"
                    }
                }
            }
            if (theCity != null) {
                if (theCity!!.isNotEmpty()) {
                    address = if (address != null) {
                        "$address, $theCity"
                    } else {
                        "$theCity"
                    }
                }
            }
            if (thePrincipalSubdivision != null) {
                if (thePrincipalSubdivision!!.isNotEmpty()) {
                    address = if (address != null) {
                        "$address, $thePrincipalSubdivision"
                    } else {
                        "$thePrincipalSubdivision"
                    }
                }
            }
            if (theCountryCode != null) {
                if (theCountryCode!!.isNotEmpty()) {
                    address = if (address != null) {
                        "$address, $theCountryCode"
                    } else {
                        "$theCountryCode"
                    }
                }
            }
            if (theContinent != null) {
                if (theContinent!!.isNotEmpty()) {
                    address = if (address != null) {
                        "$address, $theContinent"
                    } else {
                        "$theContinent"
                    }
                }
            }

            readableAddress.text = address
            gpsLocationTI.setEndIconDrawable(R.drawable.ic_content_copy)

        }, { _ ->
            Toast.makeText(this, "Response Error catch", Toast.LENGTH_LONG).show()
        }

        )
        // Access the RequestQueue through your singleton class.
        // Add the request to the RequestQueue.
        requestQueue.add(jsonObjectRequest)
    }

    private fun convertToDegree(stringDMS: String): Float {
        val result: Float?
        val dMS = stringDMS.split((",").toRegex(), 3).toTypedArray()
        val stringD = dMS[0].split(("/").toRegex(), 2).toTypedArray()
        val d0: Double = stringD[0].toDouble()
        val d1: Double = stringD[1].toDouble()
        val floatD = d0 / d1
        val stringM = dMS[1].split(("/").toRegex(), 2).toTypedArray()
        val m0: Double = stringM[0].toDouble()
        val m1: Double = stringM[1].toDouble()
        val floatM = m0 / m1
        val stringS = dMS[2].split(("/").toRegex(), 2).toTypedArray()
        val s0: Double = stringS[0].toDouble()
        val s1: Double = stringS[1].toDouble()
        val floatS = s0 / s1
        result = (floatD + floatM / 60 + floatS / 3600).toFloat()
        return result
    }

}
