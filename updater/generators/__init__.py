# __init__ file for generators module
# @author Daniel J. Finnegan
# @date September 2017

Generators = [
'C++',
'Unity',
'LaTeX',
'R',
]

__all__ = [
'base_gen',
'cpp',
'unity',
'latex',
'r',
]

# Update this function with every new generator
def load_generator(generator_name, project_root_path):
	if generator_name == 'Unity':
		project_generator = unity.UnityGenerator(project_root_path)
	elif generator_name == 'C++':
		project_generator = cpp.CppGenerator(project_root_path)
	elif generator_name == 'LaTeX':
		project_generator = latex.LatexGenerator(project_root_path)
	elif generator_name == 'R':
		project_generator = r.RGenerator(project_root_path)
	# elif generator_name == '<insert_new_generator_here>':
	#     project_generator = <New>Generator(self.project_root_text.get())
	else:
		project_generator = base_gen.ProjectGenerator(project_root_path)

	return project_generator