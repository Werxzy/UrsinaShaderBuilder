

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
    'vec' : ['vec2', 'vec3', 'vec4'],
    'mat' : ['mat2', 'mat3', 'mat4'],
    'ivec' : ['ivec2', 'ivec3', 'ivec4'],
    'bvec' : ['bvec2', 'bvec3', 'bvec4'],
    'genType' : ['float', 'vec2', 'vec3', 'vec4'],
}
   

# http://mew.cx/glsl_quickref.pdf (bless) (probably outdated and bit unrelated to panda3d)

'''
holds all base instructions
'''
# for key, value in GLSL.items: # probably not needed in this way, but just in case


def simple_func(desc, func, types = ['genType']):
    return {
        'description' : desc, 
        'inputs' : {'a_': list(types)}, 
        'outputs': {'result': list(types)}, 
        'function' : 'result=' + func + '(a_);'
        }

def build_func(desc, func, names = 'abcdef', inputTypes = [['genType'],], outputTypes = ['genType']):
    re = {
        'description' : desc, 
        'inputs' : {}, 
        'outputs': {'result': outputTypes}, 
        'function' : 'result=' + func + '('
        }

    for i in range(len(inputTypes)):
        v = names[i]
        if len(v) == 1:
            v += '_'
        re['inputs'].update({v : inputTypes[i]})
        if i > 0: 
            re['function'] += ','
        re['function'] += v
    
    re['function'] += ');'

    return re


# instructions like swizzle might need special nodes
# how do loops if needed?

'''

be careful with input/output names in the function, as they might replace the incorrect things

'INSTRUCTION NAME' : {
    'description' : '',				# text describing the instruction
    'inputs' : { 					# lists all the inputs and their name
        'INPUT NAME' : ['TYPE'] 	# input name and list of possible types (!!! Nth value in each array is paired together, even in output )
    },
    'outputs' : {					# lists all the outputs and their name (there's almost always only one, but with 'out' there could be multiple)
        'OUTPUT NAME' : ['TYPE']  	# output name and list of possible types
    },
    'function : 'FUNCTION',			# function used to put into GLSL (using str.replace using input names)
}


currently assumes there will be only one of DataMultiTypes in any ith inputs or outputs types
    (there can be genType in all inputs and outputs, but no genType and vec together)

if there's only outputs, there should only be one
    this can be changed, but would need reworking of ShaderNode.update_connections and what GLSL[]['funciton'] stores

'''
GLSL = {

# Arithmatic instructions

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
    
# Angle and trigonometry functions

    'Sine' : simple_func('Sine math function.', 'sin'),
    'Cosine' : simple_func('Cosine math function.', 'cos'),
    'Tangent' : simple_func('Tangent math function.', 'tan'),
    'Arcsine' : simple_func('Arcsine math function.', 'asin'),
    'Arccosine' : simple_func('Arccosine math function.', 'acos'),
    'Arctangent' : simple_func('Arctangent math function.', 'atan'),
    'Arctangent 2' : {
        'description' : 'Arctangent math function using\nseperate x and y inputs.', 
        'inputs' : {'y': ['genType'], 'x': ['genType']}, 
        'outputs': {'result': ['genType']}, 
        'function' : 'result=atan(y,x);'
        },

    'Radians' : simple_func('Converts degrees to radians.', 'radians'),
    'Degrees' : simple_func('Converts radians to degrees.', 'degrees'),
    
# Exponential functions
    
    'Power' : build_func('Math function being a^b.', 'pow', inputTypes=[['genType'], ['genType']]),
    'Exponent' : simple_func('Natural exponential.', 'exp'),
    'Logarithm' : simple_func('Natural logarithm.', 'log'),
    'Exponent 2' : simple_func('Finds 2^return = a', 'exp2'),
    'Square Root' : simple_func('Square root.', 'sqrt'),
    'Inverse Square Root' : simple_func('Inverse square root.', 'inversesqrt'),

# Common functions

    'Absolute' : simple_func('Removes the sign of a value.', 'abs'),
    'Ceiling' : simple_func('Rounds the value(s) up.', 'ceil'),
    'Clamp' : build_func('Clamps a value or vector\nbetween a minimum and maximum.', 'clamp', 
        names=['input_', 'min_', 'max_'],
        inputTypes=[['genType','genType'], ['genType','float'], ['genType','float']], 
        outputTypes=['genType','genType']),
    
    'Floor' : simple_func('Rounds the value(s) down.', 'floor'),
    'Fraction' : simple_func('Gets the decimal values.', 'frac'),
    'Maximum' : build_func('Gets the maximum value(s).', 'max', inputTypes=[['genType','genType'], ['genType','float']], outputTypes=['genType','genType']),
    'Minimum' : build_func('Gets the minimum value(s).', 'min', inputTypes=[['genType','genType'], ['genType','float']], outputTypes=['genType','genType']),
    'Interpolate' : build_func('Linearly interpolates between\n two values.', 'mix', names=['from_', 'to_', 'T_'],
        inputTypes=[['genType','genType'], ['genType','genType'], ['genType','float']], 
        outputTypes=['genType','genType']),

    'Modulous' : build_func('Gets the remainder of\n dividing by a value.', 'mod', inputTypes=[['genType','genType'], ['genType','float']], outputTypes=['genType','genType']),
    'Sign' : simple_func('Gets the sign of a value', 'sign'),
    'Smooth Step' : build_func('Smoothly interpolates between 0 and 1.\n(I think?)', 'smoothstep', names=['edge_a_', 'edge_b_', 'x_'],
        inputTypes=[['genType','float'], ['genType','float'], ['genType','genType']], 
        outputTypes=['genType','genType']),
    
    'Step' : build_func('Gives 0 where x is smaller,\n otherwise gives 1.', 'step', names=['edge_', 'x_'],
        inputTypes=[['genType','float'], ['genType','genType']], outputTypes=['genType','genType']),

# Geometric functions

    'ftransform':{
        'description' : 'I don\'t know?\nFragment shader only.', 
        'inputs' : {},
        'outputs' : {'result': ['vec4']}, 
        'function' : 'result=ftransform();'
    },
    'Cross Product' : build_func('Cross product of two vectors.', 'cross', inputTypes=[['vec3'], ['vec3']], outputTypes=['vec3']),
    'Distance' : build_func('Distance between two values.', 'distance', inputTypes=[['genType'], ['genType']], outputTypes=['float']),
    'Dot Product' : build_func('Dot product of two values.', 'dot', inputTypes=[['genType'], ['genType']], outputTypes=['float']),
    'Face Forward' : build_func('Flips Direction of V\n if I and N face differently.', 'dot', names='VIN', inputTypes=[['genType'], ['genType'], ['genType']], outputTypes=['genType']),
    'Length' : build_func('Length of the vector', 'length', inputTypes=[['genType']], outputTypes=['float']),
    'Normalize' : build_func('Normalizes the vector.', 'normalize', inputTypes=[['genType']], outputTypes=['genType']),
    'Reflect' : build_func('Reflects a vector.', 'reflect', names=['_in', '_normal'], inputTypes=[['genType'], ['genType']], outputTypes=['genType']),
    'Refract' : build_func('Refracts a vector.', 'refract', names=['_in', '_normal', '_eta'], inputTypes=[['genType'], ['genType'], ['float']], outputTypes=['genType']),
}


#expands the genType for every version of the function
for inst in GLSL.values():
    c = 0
    l = list(inst['inputs'].values())
    if(len(l) > 0):
        c = l[0]
    else:
        c = list(inst['outputs'].values())[0]

    for _ in range(len(c)):

        inouts = [('inputs', k, v.pop(0)) for k,v in inst['inputs'].items()]
        inouts += [('outputs', k, v.pop(0)) for k,v in inst['outputs'].items()]

        found = ''
        for i in inouts:
            if i[2] in DataMultiTypes.keys():
                found = i[2]
                break
        
        if found != '':
            for _ in range(len(inouts)):
                orig = inouts.pop(0)
                if orig[2] == found:
                    inouts += [(orig[0], orig[1], v) for v in DataMultiTypes[found]]
                else:
                    inouts += [orig for _ in DataMultiTypes[found]]

        for v in inouts:
            inst[v[0]][v[1]].append(v[2])
    
    # remove duplicates, if input[i] == input[j]: input.pop(i), output.pop(i)
    # only checks inputs, because there shouldn't be any duplicate input data types with different outputs data types
    for i in range(len(c) - 1, 0, -1):
        keys_i = list(inst['inputs'].keys())
        
        for j in range(i - 1):
            dupe = True
            
            for k in keys_i:
                if inst['inputs'][k][i] != inst['inputs'][k][j]:
                    dupe = False
                    break
            
            if dupe:
                for k in keys_i:
                    inst['inputs'][k].pop(i)
                for k in inst['outputs'].keys():
                    inst['outputs'][k].pop(i)
    
        
'''
( example )

'Clamp' : {
    'description': 'Clamps a value or vector\nbetween a minimum and maximum.', 
    'inputs': {
        'input': ['genType','genType'],
        'min': ['genType','float'], 
        'max': ['genType','float']}, 
    'outputs': {
        'result': ['genType','genType']}, 
    'function' : 'result=clamp(input,min,max);'
}

( turns into )

'Clamp' : {
    'description': 'Clamps a value or vector\nbetween a minimum and maximum.', 
    'inputs': {
        'input' : ['float', 'vec2', 'vec3', 'vec4', 'vec2', 'vec3', 'vec4'], 
        'min': ['float', 'vec2', 'vec3', 'vec4', 'float', 'float', 'float'], 
        'max': ['float', 'vec2', 'vec3', 'vec4', 'float', 'float', 'float']}, 
    'outputs': {
        'result': ['float', 'vec2', 'vec3', 'vec4', 'vec2', 'vec3', 'vec4']}, 
    'function': 'result=clamp(input,min,max);'
}

( there ARE duplicates, don't think it matters for now )
'''
