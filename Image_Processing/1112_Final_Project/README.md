# Introduction to Digital Image Processing - Final Project

## Intro
- Course info：NCHU 1112 Introduction to Image Processing
- Content：Here is the python implementation (by EEGuizhi) code of the below paper, and this is the final project of the course above.

## Paper
- Title：
    "<i>Progressive color transfer for images of arbitrary dynamic range</i>"
- Ref：<br>
    ![](image.png)


## Color Transfer Example
- Source： ![](source/source_01.jpg)
- Target： ![](target/target_01.jpg)
- Results：
    - 100% Transfer： ![](output/ColorTransfer_perc100.png)
    - 75% Transfer： ![](output/ColorTransfer_perc75.png)
    - 50% Transfer： ![](output/ColorTransfer_perc50.png)


## Things that confuse me (& how I deal with)
- The `perc/Smax` term in the line `for each level k in perc/Smax` in pseudo code is very weird,
I change it into `perc * Smax`.

- $S_{max}$ (Eq.7) of source and target images (histogram) should be the same,
and $B_{min}$ (in Eq.7) should be same too, so bins ($B$) amount of source and target are same.

- Width $V$ of bins of $H_s$ and $H_t$ are same. If they are not, the program will be more complicated to meet first requirement.

- Because of above statments, $min(I)$ and $max(I)$ of source and target images are same. $min(I)$ and $max(I)$ refer to the lowest and highest possible value of image.

- Eq.12 is very weird because $h_{o, k}$ doesn't exist when $k = S_{max}$ (at the same time $w_{s, k} = 0$). <br> So I rewrite the equation：
$$h_{o, k} = (h_{s, k}-\mu_{s, k}) \times \frac{w_{t, k}．\sigma_{t, k} + w_{s, k}．\sigma_{s, k}}{\sigma_{s, k}} + w_{t, k}．\mu_{t, k} + w_{s, k}．\mu_{s, k}$$ <br>

- When RegionTransfer function only transfer one bin, std ($\sigma$) will equals to 0 at the same time. <br> So equation will become： $$h_{o, k} = (h_{s, k}-\mu_{s, k}) + w_{t, k}．\mu_{t, k} + w_{s, k}．\mu_{s, k}$$ <br> (Remove the std term to avoid divided by zero problem.)

