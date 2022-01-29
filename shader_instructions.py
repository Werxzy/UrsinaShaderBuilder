

# this may need to represent in a better way
DataTypes = [
	'bool',
	'int',
	'float',
	'vec2',
	'vec3',
	'vec4',
	'ivec2',
	'ivec3',
	'ivec4',
	'bvec2',
	'bvec3',
	'bvec4',
	'mat2',
	'mat3',
	'mat4',

	'sampler1D',
	'sampler2D',
	'sampler3D',
	'samplerCube',
	'sampler1DShadow',
	'sampler2DShadow',
]

DataMultiTypes = {
	'vec' : ('vec2', 'vec3', 'vec4'),
	'mat' : ('mat2', 'mat3', 'mat4'),
	'ivec' : ('ivec2', 'ivec3', 'ivec4'),
	'bvec' : ('bvec2', 'bvec3', 'bvec4'),
	'genType' : ('float', 'vec2', 'vec3', 'vec4'),
}
   

# http://mew.cx/glsl_quickref.pdf (bless)

'''
holds all base instructions
'''
# for key, value in GLSL.items: # probably not needed in this way, but just in case





# instructions like swizzle might need special nodes
# how do loops if needed?

'''

be careful with input/output names in the function, as they might replace the incorrect things
could change the types and just have any inputs set to the best fitting gentype? (may be difficult)

'INSTRUCTION NAME' : {
	'description' : '',				# text describing the instruction
	'inputs' : { 					# lists all the inputs and their name
		'INPUT NAME' : ['TYPE'] 	# input name and list of possible types (!!! Nth value in each tuple is paired together, even in output )
	},
	'outputs' : {					# lists all the outputs and their name (there's almost always only one, but with 'out' there could be multiple)
		'OUTPUT NAME' : ['TYPE']  	# output name and list of possible types
	},
	'function : 'FUNCTION',			# function used to put into GLSL (using str.replace using input names)
}


'''
GLSL = {
	'Add' : {
		'description' : 'Add two values.', 
		'inputs' : {'a': ['genType'],'b': ['genType']}, 
		'outputs': {'result': ['genType']}, 
		'function' : 'result=a+b;'
		},
	'Subtract' : {
		'description' : 'Subtract a value by another.', 
		'inputs' : {'a': ['genType'],'b': ['genType']}, 
		'outputs': {'result': ['genType']}, 
		'function' : 'result=a-b;'
		},
	'Multiply' : {
		'description' : 'Multiply two values.', 
		'inputs' : {'a': ['genType'],'b': ['genType']}, 
		'outputs': {'result': ['genType']}, 
		'function' : 'result=a*b;'
		},
	'Divide' : {
		'description' : 'Divide a value by another.', 
		'inputs' : {'a': ['genType'],'b': ['genType']}, 
		'outputs': {'result': ['genType']}, 
		'function' : 'result=a/b;'
		},

	'Clamp' : {
		'description' : 'Clamps a value or vector\nbetween a minimum and maximum.', 
		'inputs' : {'input': ['genType','genType'],'min': ['genType','float'], 'max': ['genType','float']}, 
		'outputs': {'result': ['genType','genType']}, 
		'function' : 'result=clamp(input,min,max);'
		},
}



