# Introduction to Digital Image Processing (Final Project)

## Final Project：
- Title：
    "Progressive color transfer for images of arbitrary dynamic range"
- Ref：<br>
    ![](image.png)


## Color Transfer Example：
- Source： ![](source/source_01.jpg)
- Target： ![](target/target_01.jpg)
- Results：
    - 100% Transfer： ![](output/ColorTransfer_perc100.png)
    - 75% Transfer： ![](output/ColorTransfer_perc75.png)
    - 50% Transfer： ![](output/ColorTransfer_perc50.png)


## Things that confuse me：
- $S_{max}$ (Eq.7) of source and target images (histogram) should be the same,
and $B_{min}$ (in Eq.7) should be same too, so bins amount of source and target are same.

- Width $V$ of bins of $H_s$ and $H_t$ are same. If they are not, the program will be more complicated to meet first requirement.

- Because of above things, $min(I)$ and $max(I)$ of source and target images are same. $min(I)$ and $max(I)$ refer to the lowest and highest possible value of image.

- Eq.12 is very weird because $w_{t, k} = 1$ and $w_{s, k} = 0$ when $k = S_{max}$, and then, $h_{o, k}$ doesn't exist.<br>So I rewrite the equation：
$$ h_{o, k} = (h_{s, k}-\mu_{s, k}) \times \frac{w．\sigma_{t, k} + (1-w)．\sigma_{s, k}}{\sigma_{s, k}} + w．\mu_{t, k} + (1-w)．\mu_{s, k} $$

- When RegionTransfer function only transfer one bin, std ($\sigma$) will equals to 0 at the same time. <br> So equation will become (avoid divide by 0)： $$ h_{o, k} = (h_{s, k}-\mu_{s, k}) + w．\mu_{t, k} + (1-w)．\mu_{s, k} $$ <br>

