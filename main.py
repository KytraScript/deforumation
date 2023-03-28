import wx
import os
deforumSettingsPath="E:\\prompt.txt"
deforumSettingsLockFilePath = "E:\\prompt.txt.locked"
Prompt_Positive = ""
Prompt_Negative = ""
Strength_Scheduler = 0.65
Translation_X = 0.0
Translation_Y = 0.0
Translation_Z = 0.0
Rotation_3D_X = 0.0
Rotation_3D_Y = 0.0
Rotation_3D_Z = 0.0
tbrY = 420
trbX = 50

def lock():
    try:
        with open(deforumSettingsLockFilePath, 'x') as lockfile:
            # write the PID of the current process so you can debug
            # later if a lockfile can be deleted after a program crash
            lockfile.write(str(os.getpid()))
            lockfile.close()
            return True
    except IOError:
         # file already exists
        print("ALREADY LOCKED")
        return False
def unlock():
    os.remove(deforumSettingsLockFilePath)

class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(700, 700))
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(100, 100, 100))
        #Positive Prompt
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.positivePromtText = wx.StaticText(panel, label="Positive prompt:")
        font = self.positivePromtText.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.positivePromtText.SetFont(font)
        sizer.Add(self.positivePromtText, 0, wx.ALL | wx.EXPAND, 5)
        self.positive_prompt_input_ctrl = wx.TextCtrl(panel,style=wx.TE_MULTILINE, size=(-1,100))
        sizer.Add(self.positive_prompt_input_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        #Negative Prompt
        self.negativePromtText = wx.StaticText(panel, label="Negative prompt:")
        font = self.negativePromtText.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.negativePromtText.SetFont(font)
        sizer.Add(self.negativePromtText, 0, wx.ALL | wx.EXPAND, 5)

        self.negative_prompt_input_ctrl = wx.TextCtrl(panel,style=wx.TE_MULTILINE, size=(-1,100))
        sizer.Add(self.negative_prompt_input_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        #SAVE PROMPTS BUTTON
        self.update_prompts = wx.Button(panel, label="SAVE PROMPTS")
        sizer.Add(self.update_prompts, 0, wx.ALL | wx.EXPAND, 5)
        self.update_prompts.Bind(wx.EVT_BUTTON, self.OnClicked)

        panel.SetSizer(sizer)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        #PAN STEPS INPUT
        self.pan_step_input_box = wx.TextCtrl(panel, size=(40,20), pos=(trbX-15, 30+tbrY))
        self.pan_step_input_box.SetLabel("1.0")

        #LEFT PAN BUTTTON
        bmp = wx.Bitmap(".\\images\\left_arrow.bmp", wx.BITMAP_TYPE_BMP)
        self.transform_x_left_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(5+trbX, 55+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.transform_x_left_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.transform_x_left_button.SetLabel("PAN_LEFT")

        #SET PAN VALUE X
        self.pan_X_Value_Text = wx.StaticText(panel, label=str(Translation_X), pos=(trbX-26, 55+tbrY+5))
        font = self.pan_X_Value_Text.GetFont()
        font.PointSize += 1
        font = font.Bold()
        self.pan_X_Value_Text.SetFont(font)

        #SET PAN VALUE Y
        self.pan_Y_Value_Text = wx.StaticText(panel, label=str(Translation_Y), pos=(40+trbX, 5+tbrY))
        font = self.pan_Y_Value_Text.GetFont()
        font.PointSize += 1
        font = font.Bold()
        self.pan_Y_Value_Text.SetFont(font)

        #UPP PAN BUTTTON
        bmp = wx.Bitmap(".\\images\\upp_arrow.bmp", wx.BITMAP_TYPE_BMP)
        self.transform_y_upp_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(35+trbX, 25+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.transform_y_upp_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.transform_y_upp_button.SetLabel("PAN_UP")
        #RIGHT PAN BUTTTON
        bmp = wx.Bitmap(".\\images\\right_arrow.bmp", wx.BITMAP_TYPE_BMP)
        self.transform_x_right_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(65+trbX, 55+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.transform_x_right_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.transform_x_right_button.SetLabel("PAN_RIGHT")
        #DOWN PAN BUTTTON
        bmp = wx.Bitmap(".\\images\\down_arrow.bmp", wx.BITMAP_TYPE_BMP)
        self.transform_y_down_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(35+trbX, 85+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.transform_y_down_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.transform_y_down_button.SetLabel("PAN_DOWN")

        #ZOOM SLIDER
        self.zoom_slider = wx.Slider(panel, id=wx.ID_ANY, value=0, minValue=-10, maxValue=10, pos = (110+trbX, tbrY-5), size = (40, 150), style = wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_INVERSE )
        self.zoom_slider.Bind(wx.EVT_SCROLL, self.OnClicked)
        self.zoom_slider.SetTickFreq(1)
        self.zoom_slider.SetLabel("ZOOM")
        self.ZOOM_X_Text = wx.StaticText(panel, label="Z", pos=(170+trbX, tbrY+40))
        self.ZOOM_X_Text2 = wx.StaticText(panel, label="O", pos=(170+trbX, tbrY+60))
        self.ZOOM_X_Text3 = wx.StaticText(panel, label="O", pos=(170+trbX, tbrY+80))
        self.ZOOM_X_Text4 = wx.StaticText(panel, label="M", pos=(169+trbX, tbrY+100))

        #STRENGTH SCHEDULE SLIDER
        self.strength_schedule_slider = wx.Slider(panel, id=wx.ID_ANY, value=65, minValue=1, maxValue=100, pos = (trbX-25, tbrY-50), size = (300, 40), style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
        self.strength_schedule_slider.Bind(wx.EVT_SCROLL, self.OnClicked)
        self.strength_schedule_slider.SetTickFreq(1)
        self.strength_schedule_slider.SetLabel("STRENGTH SCHEDULE")
        self.ZOOM_X_Text = wx.StaticText(panel, label="Strength Value - (slider value is divided by 100)", pos=(trbX-35, tbrY-70))

        #LOOK LEFT BUTTTON
        bmp = wx.Bitmap(".\\images\\look_left.bmp", wx.BITMAP_TYPE_BMP)
        self.rotation_3d_x_left_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(240+trbX, 55+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.rotation_3d_x_left_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rotation_3d_x_left_button.SetLabel("LOOK_LEFT")

        #SET ROTATION VALUE X
        self.rotation_3d_x_Value_Text = wx.StaticText(panel, label=str(Rotation_3D_X), pos=(240+trbX-30, 55+tbrY+5))
        font = self.rotation_3d_x_Value_Text.GetFont()
        font.PointSize += 1
        font = font.Bold()
        self.rotation_3d_x_Value_Text.SetFont(font)

        #ROTATE STEPS INPUT
        self.rotate_step_input_box = wx.TextCtrl(panel, size=(40,20), pos=(240+trbX-15, 30+tbrY))
        self.rotate_step_input_box.SetLabel("1.0")

        #LOOK UPP BUTTTON
        bmp = wx.Bitmap(".\\images\\look_upp.bmp", wx.BITMAP_TYPE_BMP)
        self.rotation_3d_y_up_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(240+trbX+30, 55+tbrY-30), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.rotation_3d_y_up_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rotation_3d_y_up_button.SetLabel("LOOK_UP")

        #SET ROTATION VALUE Y
        self.rotation_3d_y_Value_Text = wx.StaticText(panel, label=str(Rotation_3D_Y), pos=(240+trbX+35, 55+tbrY-48))
        font = self.rotation_3d_y_Value_Text.GetFont()
        font.PointSize += 1
        font = font.Bold()
        self.rotation_3d_y_Value_Text.SetFont(font)

        #LOOK RIGHT BUTTTON
        bmp = wx.Bitmap(".\\images\\look_right.bmp", wx.BITMAP_TYPE_BMP)
        self.rotation_3d_x_right_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(240+trbX+57, 55+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.rotation_3d_x_right_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rotation_3d_x_right_button.SetLabel("LOOK_RIGHT")

        #LOOK UPP BUTTTON
        bmp = wx.Bitmap(".\\images\\look_down.bmp", wx.BITMAP_TYPE_BMP)
        self.rotation_3d_y_down_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(240+trbX+30, 55+tbrY+30), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.rotation_3d_y_down_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rotation_3d_y_down_button.SetLabel("LOOK_DOWN")

        #ROTATE LEFT BUTTTON
        bmp = wx.Bitmap(".\\images\\rotate_left.bmp", wx.BITMAP_TYPE_BMP)
        self.rotation_3d_z_right_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(300+trbX+57, 50+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.rotation_3d_z_right_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rotation_3d_z_right_button.SetLabel("ROTATE_LEFT")

        #ROTATE RIGHT BUTTTON
        bmp = wx.Bitmap(".\\images\\rotate_right.bmp", wx.BITMAP_TYPE_BMP)
        self.rotation_3d_z_right_button = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp, pos=(380+trbX+57, 50+tbrY), size=(bmp.GetWidth() + 10, bmp.GetHeight() + 10))
        self.rotation_3d_z_right_button.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rotation_3d_z_right_button.SetLabel("ROTATE_RIGHT")

        #SET ROTATION VALUE Z
        self.rotation_Z_Value_Text = wx.StaticText(panel, label=str(Rotation_3D_Z), pos=(360+trbX+46, 60+tbrY))
        font = self.rotation_Z_Value_Text.GetFont()
        font.PointSize += 1
        font = font.Bold()
        self.rotation_Z_Value_Text.SetFont(font)

        #TILT STEPS INPUT
        self.tilt_step_input_box = wx.TextCtrl(panel, size=(40,20), pos=(360+trbX+38, 30+tbrY))
        self.tilt_step_input_box.SetLabel("1.0")

        self.Centre()
        self.Show()
        self.Fit()

    def OnClicked(self, event):
        global Translation_X
        global Translation_Y
        global Translation_Z
        global Rotation_3D_X
        global Rotation_3D_Y
        global Rotation_3D_Z
        global Strength_Scheduler
        btn = event.GetEventObject().GetLabel()
        print("Label of pressed button = ", btn)
        if btn == "PAN_LEFT":
            Translation_X = Translation_X - float(self.pan_step_input_box.GetValue())
        elif btn == "PAN_RIGHT":
            Translation_X = Translation_X + float(self.pan_step_input_box.GetValue())
        elif btn == "PAN_UP":
            Translation_Y = Translation_Y + float(self.pan_step_input_box.GetValue())
        elif btn == "PAN_DOWN":
            Translation_Y = Translation_Y - float(self.pan_step_input_box.GetValue())
        elif btn == "ZOOM":
            Translation_Z = self.zoom_slider.GetValue()
        elif btn == "STRENGTH SCHEDULE":
            Strength_Scheduler = float(self.strength_schedule_slider.GetValue())*0.01
        elif btn == "LOOK_LEFT":
            Rotation_3D_Y = Rotation_3D_Y - float(self.rotate_step_input_box.GetValue())
        elif btn == "LOOK_RIGHT":
            Rotation_3D_Y = Rotation_3D_Y + float(self.rotate_step_input_box.GetValue())
        elif btn == "LOOK_UP":
            Rotation_3D_X = Rotation_3D_X + float(self.rotate_step_input_box.GetValue())
        elif btn == "LOOK_DOWN":
            Rotation_3D_X = Rotation_3D_X - float(self.rotate_step_input_box.GetValue())
        elif btn == "ROTATE_LEFT":
            Rotation_3D_Z = Rotation_3D_Z + float(self.tilt_step_input_box.GetValue())
        elif btn == "ROTATE_RIGHT":
            Rotation_3D_Z = Rotation_3D_Z - float(self.tilt_step_input_box.GetValue())



        self.pan_X_Value_Text.SetLabel(str('%.2f' % Translation_X))
        self.pan_Y_Value_Text.SetLabel(str('%.2f' % Translation_Y))
        self.rotation_3d_x_Value_Text.SetLabel(str('%.2f' % Rotation_3D_Y))
        self.rotation_3d_y_Value_Text.SetLabel(str('%.2f' %Rotation_3D_X))
        self.rotation_Z_Value_Text.SetLabel(str('%.2f' %Rotation_3D_Z))
        if lock():
            deforumFile = open(deforumSettingsPath, 'w')
            deforumFile.write(self.positive_prompt_input_ctrl.GetValue().strip().replace('\n', '')+"\n")
            deforumFile.write(self.negative_prompt_input_ctrl.GetValue().strip().replace('\n', '')+"\n")
            deforumFile.write(str('%.2f' % Strength_Scheduler)+"\n")
            deforumFile.write(str('%.2f' % Translation_X)+"\n")
            deforumFile.write(str('%.2f' % Translation_Y)+"\n")
            deforumFile.write(str('%.2f' % Translation_Z)+"\n")
            deforumFile.write(str('%.2f' % Rotation_3D_X)+"\n")
            deforumFile.write(str('%.2f' % Rotation_3D_Y)+"\n")
            deforumFile.write(str('%.2f' % Rotation_3D_Z)+"\n")
            deforumFile.close()
            unlock()


    def OnToggle(self, event):
        state = event.GetEventObject().GetValue()

        if state == True:
            print("Toggle button state off")
            event.GetEventObject().SetLabel("click to off")
        else:
            print(" Toggle button state on")
            event.GetEventObject().SetLabel("click to on")

if __name__ == '__main__':
    app = wx.App()
    Mywin(None, 'Button demo')
    app.MainLoop()
