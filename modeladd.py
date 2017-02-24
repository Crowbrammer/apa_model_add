# Get the unused machines screen done
import libs.apa_database
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


class ScreenManagement(ScreenManager):
	pass

class ModelAddScreen(Screen):
	pass

class ModelAddLayout(BoxLayout):

	def __init__(self, **kwargs):
		super(ModelAddLayout, self).__init__(**kwargs)
		Clock.schedule_once(self.late_init, 0)

	def late_init(self, key, **largs):
		# print(dir(self.ids.num_positions))
		test = self.ids.model_add_name.text
		# print('test: ',str(test))
		# create a dropdown with 10 buttons
		dropdown = DropDown()
		for index in range(1,11):
			# When adding widgets, we need to specify the height manually
			# (disabling the size_hint_y) so the dropdown can calculate
			# the area it needs.

			btn = Button(text='%d' % index, size_hint_y=None, height=44)

			# for each button, attach a callback that will call the select() method
			# on the dropdown. We'll pass the text of the button as the data of the
			# selection.
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))

			# then add the button inside the dropdown
			dropdown.add_widget(btn)

		self.ids.num_positions.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x, e=self.ids.num_positions: setattr(e, 'text', x))



	def record_new_model(self):
		model_name = self.ids.model_add_name.text
		try:
			num_positions = int(self.ids.num_positions.text)
		except ValueError:
			self.ids.num_positions.text = 'Please select # of positions for model:'
			return
		print(model_name)
		print('num_positions: ' + str(num_positions))

		for i in range(1, num_positions + 1):
			libs.apa_database.insert_data(tb='modelID_positionnum', col1='modelID', \
			 		data1=model_name, col2='positionNum', data2=i)

class PrimaryOverlay(ScrollView):
	pass

class AppWideHUD(BoxLayout):
	pass

class ModelAddApp(App):
	pass

# A
if __name__ == '__main__':
	ModelAddApp().run()
