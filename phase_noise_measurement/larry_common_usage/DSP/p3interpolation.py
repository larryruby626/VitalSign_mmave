

def P3InterpolateDer(p_l, p_c, p_u):
    xl = p_l[0]
    yl = p_l[1]
    xc = p_c[0]
    yc = p_c[1]
    xu = p_u[0]
    yu = p_u[1]
    d0 = yc
    d2 = 2 * ((yu - yc) / (xu - xc) - (yl - yc) / (xl - xc)) / (xu - xl)
    if ((xu+xl)>=(xc+xc)):
        d1 = (yu-yc)/(xu-xc) - 0.5*d2*(xu-xc)
    else:
        d1 = (yc-yl)/(xc-xl) + 0.5*d2*(xc-xl)

    if (d2):
        xe = xc - d1 / d2;
        ye = yc + 0.5 * d1 * (xe-xc)
    x = []
    y = []
    for i in range(128):
        x.append(i)
        y_tmp = (d2 / 2) * ((int(i) - xc)^ 2) + d1 * (int(i) - xc) + d0
        y.append(y_tmp)

    return xe, ye, x, y



