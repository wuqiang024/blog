# BottomSheetDialog
***
要制作从底部弹出的弹框，可使用该方法

1、引入依赖
```gradle
implementation 'com.google.android.material:material:1.2.0'
```

2、主要代码
```java
private lateinit var bottomSheetDialog: BottomSheetDialog
    private lateinit var mDialogBehavior: BottomSheetBehavior<View>
override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        btn.setOnClickListener {
            showSheetDialog()
        }
    }

  private fun showSheetDialog() {
      var view1: View = LayoutInflater.from(this).inflate(R.layout.dialog_bottomsheet, null)
      // 下面代码R.style.Theme_AppCompat_Dialog加上的话，在android5下面会跟屏幕有间隙，可以考虑删除调
      bottomSheetDialog = BottomSheetDialog(this, R.style.Theme_AppCompat_Dialog)
      bottomSheetDialog.setContentView(view1)
      mDialogBehavior = BottomSheetBehavior.from(view1.parent as View)
      mDialogBehavior.setPeekHeight(getPeekHeight())
      bottomSheetDialog.show()
  }

  private fun getPeekHeight(): Int {
      val peekHeight: Int = resources.displayMetrics.heightPixels
      return peekHeight - peekHeight / 3 as Int
  }
```