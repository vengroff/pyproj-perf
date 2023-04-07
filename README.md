This project is a small repro case for a 
performance regression that I believe occurred from 
version 3.4.1 to version 3.5.0 of 
[`pyproj`](https://github.com/pyproj4/pyproj). I 
discovered this when I upgraded the dependencies of 
[`censusdis`](https://github.com/vengroff/censusdis)
and the performance of plotting maps of the US
went down by two orders of magnitude. I traced the
change down to `pyproj` and stripped it down to the 
small repro script in `repro.py` in this repository.

This project uses poetry for dependency management
but if you prefer some other tool, just create a 
virtual env with python 3.9 and 
censusdis 0.12.3
and you should be good to go. Then run 

```shell
python repro.py
```

Censusdis 0.12.3 pins pyproj to version 3.4.1, which
is from before the performance regression. So the first
time you run `repro.py` it should be fast (under a second)
and produce a profiling output that looks like 
`perf-3.4.1.txt`. 

Now, upgrade `pyproj` to 3.5.0, with
e.g. 

```shell
pip install "pyproj==3.5.0"  
```

Then run 

```shell
python repro.py
```

again. This time, it will run a lot slower and you will 
get something like `perf-3.5.0.txt` as output.

If you compare the two, the 3.4.1 run looks something
like 

```
pyproj.__version__ = 3.4.1
         2678 function calls (2617 primitive calls) in 0.457 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        2    0.335    0.168    0.335    0.168 {method '_transform' of 'pyproj._transformer._Transformer' objects}
        1    0.096    0.096    0.096    0.096 {pyproj._transformer.from_crs}
        2    0.011    0.005    0.011    0.005 {built-in method shapely.lib.set_coordinates}
        2    0.005    0.002    0.005    0.002 {built-in method shapely.lib.get_coordinates}
...
```

3.5.0 looks like

```
pyproj.__version__ = 3.5.0
         2710 function calls (2649 primitive calls) in 75.326 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        2   75.181   37.591   75.181   37.591 {method '_transform' of 'pyproj._transformer._Transformer' objects}
        1    0.119    0.119    0.119    0.119 {pyproj._transformer.from_crs}
        2    0.011    0.005    0.011    0.005 {built-in method shapely.lib.set_coordinates}
        2    0.005    0.002    0.005    0.002 {built-in method shapely.lib.get_coordinates}
...
```

Notice that in both case the bulk of the run time is spent in 
`pyproj._transformer._Transformer._transform`. But in the 3.4.1
case it is 0.335 seconds and in 3.5.0 it is 75.181 seconds.
That's a slowdown of 224 times.

This is a big enough difference that it makes the 
`censusdis.maps.plot_us` function so slow that it is 
painful for users of `censusdis`.

For reference, the numbers above were generated on a
2021 MacBook Pro with an M1 Max processor and 64GB of
RAM.