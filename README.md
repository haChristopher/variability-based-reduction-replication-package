# masters-thesis
Masters Thesis



# Installation and needed tools
Install graphviz: https://graphviz.org/download/


https://github.com/jrfonseca/gprof2dot

# Usefule commands

```
go test ./…
go test -v ./... -bench=. -run=xxx -benchmem
go test ./... -bench=. -benchmem -memprofile memprofile.out -cpuprofile profile.out
```

Only run benchmark and not tests
```
go test -bench=. -run=^$ . -cpuprofile profile.out
```

Export to graph
```
dot > graph.dot
```

cannot use -cpuprofile flag with multiple packages
