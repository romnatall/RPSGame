def guess(s):
    g0,g1,g2=1,1,1
    st=s[-2:]
    s=s[:-2]
    m=1
    while True:
        st=s[-1]+st
        s=s[:-1]
        g0+=s.count(st+'0')*m
        g1+=s.count(st+'1')*m
        g2+=s.count(st+'2')*m
        m*=3
        if s.count(st)==0 or len(s)<len(st)+1:
            break
    return (g0,g1,g2)