with open('dimensionality_reduction.log') as f:
    lines = [line.strip() for line in f.readlines() if line]

with open('plugins_after_reduction', 'w') as input_file:
    plugins = []
    for line in lines:
        if 'listcomp' in line:
            plugin = line.split(' ')[-1]
            plugins.append(str(plugin))
    plugins.sort()
    input_file.write(str(plugins))
