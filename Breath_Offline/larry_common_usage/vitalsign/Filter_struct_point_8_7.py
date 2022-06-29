import numpy as np

class Filter_struct_point_8_7:
    coef = None
    cache = None
    outout = None
    tap = None
    def __init__(self, mode):
        if mode == 1:
            # self.coef = np.array((12, 17, 23, 25, 23, 17, 12))
            self.coef = np.array((0.0982, 0.1451, 0.1880, 0.2065, 0.1880, 0.1451, 0.0982))

            self.cache = np.zeros(len(self.coef))
            self.tap = 7
            self.output = 0
            '''
            
            '''
        elif mode == 2 :
            self.coef = np.array((1, 5, 8, 11, 14, 16, 17, 16, 14, 11, 8, 5, 1))
            self.cache = np.zeros(len(self.coef))
            self.tap = 13
            self.output = 0

    def run(self, input):
        self.cache = np.roll(self.cache, 1)
        self.cache[0] = input
        self.output = np.dot(self.cache, self.coef)
        return self.output

    # def set

if __name__ == '__main__':
    a = Filter_struct_point_8_7(1)
    b = Filter_struct_point_8_7(2)
    c = Filter_struct_point_8_7(1)
    c.set_coeff([0.0982, 0.1451, 0.1880, 0.2065, 0.1880, 0.1451, 0.0982])
    # print(a.coef , a.cache, a.output, a.tap)
    print(b.coef, b.cache, b.output, b.tap)
    # print(c.coef, c.cache, c.output, c.tap)
    b.cache = np.arange(13)
    print(b.coef, b.cache, b.output, b.tap)
    b.run(132)
    print(b.coef, b.cache, b.output, b.tap)

    ccc = '0	91	128	157	181	202	222	239	256	271	286	300	313	326	338	350	362	373	384	394	404	414	424	433	443	452	461	470	478	487	495	503	511	519	527	534	542	549	557	564	571	578	585	592	599	605	612	619	625	632	638	644	651	657	663	669	675	681	687	693	699	704	710	716	721	727	732	738	743	749	754	759	765	770	775	780	785	790	796	801	806	811	815	820	825	830	835	840	844	849	854	859	863	868	872	877	882	886	891	895	900	904	908	913	917	921	926	930	934	939	943	947	951	955	960	964	968	972	976	980	984	988	992	996	1000	1004	1008	1012	1016	1020	1024	1028	1031	1035	1039	1043	1047	1050	1054	1058	1062	1065	1069	1073	1077	1080	1084	1087	1091	1095	1098	1102	1105	1109	1113	1116	1120	1123	1127	1130	1134	1137	1141	1144	1147	1151	1154	1158	1161	1164	1168	1171	1174	1178	1181	1184	1188	1191	1194	1198	1201	1204	1207	1211	1214	1217	1220	1223	1227	1230	1233	1236	1239	1243	1246	1249	1252	1255	1258	1261	1264	1267	1270	1273	1277	1280	1283	1286	1289	1292	1295	1298	1301	1304	1307	1310	1313	1316	1318	1321	1324	1327	1330	1333	1336	1339	1342	1345	1348	1350	1353	1356	1359	1362	1365	1367	1370	1373	1376	1379	1381	1384	1387	1390	1393	1395	1398	1401	1404	1406	1409	1412	1415	1417	1420	1423	1425	1428	1431	1433	1436	1439	1441	1444	1447	1449	1452	1455	1457	1460	1463	1465	1468	1470	1473	1476	1478	1481	1483	1486	1488	1491	1494	1496	1499	1501	1504	1506	1509	1511	1514	1516	1519	1521	1524	1526	1529	1531	1534	1536	1539	1541	1544	1546	1549	1551	1553	1556	1558	1561	1563	1566	1568	1570	1573	1575	1578	1580	1582	1585	1587	1590	1592	1594	1597	1599	1601	1604	1606	1608	1611	1613	1615	1618	1620	1622	1625	1627	1629	1632	1634	1636	1639	1641	1643	1645	1648	1650	1652	1654	1657	1659	1661	1663	1666	1668	1670	1672	1675	1677	1679	1681	1684	1686	1688	1690	1692	1695	1697	1699	1701	1703	1706	1708	1710	1712	1714	1716	1719	1721	1723	1725	1727	1729	1732	1734	1736	1738	1740	1742	1744	1746	1749	1751	1753	1755	1757	1759	1761	1763	1765	1768	1770	1772	1774	1776	1778	1780	1782	1784	1786	1788	1790	1792	1794	1797	1799	1801	1803	1805	1807	1809	1811	1813	1815	1817	1819	1821	1823	1825	1827	1829	1831	1833	1835	1837	1839	1841	1843	1845	1847	1849	1851	1853	1855	1857	1859	1861	1863	1865	1867	1868	1870	1872	1874	1876	1878	1880	1882	1884	1886	1888	1890	1892	1894	1896	1897	1899	1901	1903	1905	1907	1909	1911	1913	1915	1916	1918	1920	1922	1924	1926	1928	1930	1931	1933	1935	1937	1939	1941	1943	1945	1946	1948	1950	1952	1954	1956	1957	1959	1961	1963	1965	1967	1968	1970	1972	1974	1976	1978	1979	1981	1983	1985	1987	1988	1990	1992	1994	1996	1997	1999	2001	2003	2005	2006	2008	2010	2012	2013	2015	2017	2019	2020	2022	2024	2026	2027	2029	2031	2033	2035	2036	2038	2040	2041	2043	2045	2047	2048	2050	2052	2054	2055	2057	2059	2060	2062	2064	2066	2067	2069	2071	2072	2074	2076	2078	2079	2081	2083	2084	2086	2088	2089	2091	2093	2094	2096	2098	2100	2101	2103	2105	2106	2108	2110	2111	2113	2115	2116	2118	2119	2121	2123	2124	2126	2128	2129	2131	2133	2134	2136	2138	2139	2141	2142	2144	2146	2147	2149	2151	2152	2154	2155	2157	2159	2160	2162	2163	2165	2167	2168	2170	2172	2173	2175	2176	2178	2179	2181	2183	2184	2186	2187	2189	2191	2192	2194	2195	2197	2198	2200	2202	2203	2205	2206	2208	2209	2211	2213	2214	2216	2217	2219	2220	2222	2223	2225	2227	2228	2230	2231	2233	2234	2236	2237	2239	2240	2242	2243	2245	2246	2248	2250	2251	2253	2254	2256	2257	2259	2260	2262	2263	2265	2266	2268	2269	2271	2272	2274	2275	2277	2278	2280	2281	2283	2284	2286	2287	2289	2290	2292	2293	2295	2296	2297	2299	2300	2302	2303	2305	2306	2308	2309	2311	2312	2314	2315	2317	2318	2319	2321	2322	2324	2325	2327	2328	2330	2331	2332	2334	2335	2337	2338	2340	2341	2343	2344	2345	2347	2348	2350	2351	2353	2354	2355	2357	2358	2360	2361	2363	2364	2365	2367	2368	2370	2371	2372	2374	2375	2377	2378	2379	2381	2382	2384	2385	2386	2388	2389	2391	2392	2393	2395	2396	2398	2399	2400	2402	2403	2404	2406	2407	2409	2410	2411	2413	2414	2415	2417	2418	2420	2421	2422	2424	2425	2426	2428	2429	2430	2432	2433	2434	2436	2437	2439	2440	2441	2443	2444	2445	2447	2448	2449	2451	2452	2453	2455	2456	2457	2459	2460	2461	2463	2464	2465	2467	2468	2469	2471	2472	2473	2475	2476	2477	2479	2480	2481	2482	2484	2485	2486	2488	2489	2490	2492	2493	2494	2496	2497	2498	2499	2501	2502	2503	2505	2506	2507	2508	2510	2511	2512	2514	2515	2516	2518	2519	2520	2521	2523	2524	2525	2526	2528	2529	2530	2532	2533	2534	2535	2537	2538	2539	2540	2542	2543	2544	2545	2547	2548	2549	2551	2552	2553	2554	2556	2557	2558	2559	2561	2562	2563	2564	2566	2567	2568	2569	2571	2572	2573	2574	2575	2577	2578	2579	2580	2582	2583	2584	2585	2587	2588	2589	2590	2591	2593	2594	2595	2596	2598	2599	2600	2601	2602	2604	2605	2606	2607	2608	2610	2611	2612	2613	2615	2616	2617	2618	2619	2621	2622	2623	2624	2625	2627	2628	2629	2630	2631	2633	2634	2635	2636	2637	2638	2640	2641	2642	2643	2644	2646	2647	2648	2649	2650	2651	2653	2654	2655	2656	2657	2659	2660	2661	2662	2663	2664	2666	2667	2668	2669	2670	2671	2673	2674	2675	2676	2677	2678	2679	2681	2682	2683	2684	2685	2686	2688	2689	2690	2691	2692	2693	2694	2696	2697	2698	2699	2700	2701	2702	2704	2705	2706	2707	2708	2709	2710	2712	2713	2714	2715	2716	2717	2718	2719	2721	2722	2723	2724	2725	2726	2727	2728	2730	2731	2732	2733	2734	2735	2736	2737	2738	2740	2741	2742	2743	2744	2745	2746	2747	2748	2750	2751	2752	2753	2754	2755	2756	2757	2758	2759	2761	2762	2763	2764	2765	2766	2767	2768	2769	2770	2771	2773	2774	2775	2776	2777	2778	2779	2780	2781	2782	2783	2784	2786	2787	2788	2789	2790	2791	2792	2793	2794	2795	2796	2797	2798	2799	2801	2802	2803	2804	2805	2806	2807	2808	2809	2810	2811	2812	2813	2814	2815	2816	2818	2819	2820	2821	2822	2823	2824	2825	2826	2827	2828	2829	2830	2831	2832	2833	2834	2835	2836	2837	2838	2840	2841	2842	2843	2844	2845	2846	2847	2848	2849	2850	2851	2852	2853	2854	2855	2856	2857	2858	2859	2860	2861	2862	2863	2864	2865	2866	2867	2868	2869	2870	2871	2872	2873	2874	2875	2876	2877	2879	2880	2881	2882	2883	2884	2885	2886	2887	2888	2889	2890	2891	2892	2893	2894	2895	2896	2897	2898	2899	2900	2901	2902	2903	2904	2905	2906	2907	2908	2909	2910	2911	2912	2913	2914	2915	2915	2916	2917	2918	2919	2920	2921	2922	2923	2924	2925	2926	2927	2928	2929	2930	2931	2932	2933	2934	2935	2936	2937	2938	2939	2940	2941	2942	2943	2944	2945	2946	2947	2948	2949	2950	2951	2952	2953	2953	2954	2955	2956	2957	2958	2959	2960	2961	2962	2963	2964	2965	2966	2967	2968	2969	2970	2971	2972	2973	2974	2974	2975	2976	2977	2978	2979	2980	2981	2982	2983	2984	2985	2986	2987	2988	2989	2990	2990	2991	2992	2993	2994	2995	2996	2997	2998	2999	3000	3001	3002	3003	3003	3004	3005	3006	3007	3008	3009	3010	3011	3012	3013	3014	3015	3015	3016	3017	3018	3019	3020	3021	3022	3023	3024	3025	3026	3026	3027	3028	3029	3030	3031	3032	3033	3034	3035	3036	3036	3037	3038	3039	3040	3041	3042	3043	3044	3045	3046	3046	3047	3048	3049	3050	3051	3052	3053	3054	3054	3055	3056	3057	3058	3059	3060	3061	3062	3062	3063	3064	3065	3066	3067	3068	3069	3070	3070	3071	3072	3073	3074	3075	3076	3077	3078	3078	3079	3080	3081	3082	3083	3084	3085	3085	3086	3087	3088	3089	3090	3091	3091	3092	3093	3094	3095	3096	3097	3098	3098	3099	3100	3101	3102	3103	3104	3104	3105	3106	3107	3108	3109	3110	3110	3111	3112	3113	3114	3115	3116	3116	3117	3118	3119	3120	3121	3122	3122	3123	3124	3125	3126	3127	3127	3128	3129	3130	3131	3132	3133	3133	3134	3135	3136	3137	3138	3138	3139	3140	3141	3142	3143	3143	3144	3145	3146	3147	3148	3148	3149	3150	3151	3152	3153	3153	3154	3155	3156	3157	3158	3158	3159	3160	3161	3162	3163	3163	3164	3165	3166	3167	3167	3168	3169	3170	3171	3172	3172	3173	3174	3175	3176	3176	3177	3178	3179	3180	3181	3181	3182	3183	3184	3185	3185	3186	3187	3188	3189	3189	3190	3191	3192	3193	3193	3194	3195	3196	3197	3197	3198	3199	3200	3201	3201	3202	3203	3204	3205	3205	3206	3207	3208	3209	3209	3210	3211	3212	3213	3213	3214	3215	3216	3217	3217	3218	3219	3220	3220	3221	3222	3223	3224	3224	3225	3226	3227	3227	3228	3229	3230	3231	3231	3232	3233	3234	3235	3235	3236	3237	3238	3238	3239	3240	3241	3241	3242	3243	3244	3245	3245	3246	3247	3248	3248	3249	3250	3251	3251	3252	3253	3254	3255	3255	3256	3257	3258	3258	3259	3260	3261	3261	3262	3263	3264	3264	3265	3266	3267	3267	3268	3269	3270	3270	3271	3272	3273	3273	3274	3275	3276	3276	3277	3278	3279	3279	3280	3281	3282	3282	3283	3284	3285	3285	3286	3287	3288	3288	3289	3290	3291	3291	3292	3293	3294	3294	3295	3296	3297	3297	3298	3299	3300	3300	3301	3302	3302	3303	3304	3305	3305	3306	3307	3308	3308	3309	3310	3311	3311	3312	3313	3313	3314	3315	3316	3316	3317	3318	3318	3319	3320	3321	3321	3322	3323	3324	3324	3325	3326	3326	3327	3328	3329	3329	3330	3331	3331	3332	3333	3334	3334	3335	3336	3336	3337	3338	3339	3339	3340	3341	3341	3342	3343	3344	3344	3345	3346	3346	3347	3348	3348	3349	3350	3351	3351	3352	3353	3353	3354	3355	3356	3356	3357	3358	3358	3359	3360	3360	3361	3362	3362	3363	3364	3365	3365	3366	3367	3367	3368	3369	3369	3370	3371	3371	3372	3373	3374	3374	3375	3376	3376	3377	3378	3378	3379	3380	3380	3381	3382	3382	3383	3384	3385	3385	3386	3387	3387	3388	3389	3389	3390	3391	3391	3392	3393	3393	3394	3395	3395	3396	3397	3397	3398	3399	3399	3400	3401	3401	3402	3403	3403	3404	3405	3405	3406	3407	3407	3408	3409	3409	3410	3411	3411	3412	3413	3413	3414	3415	3415	3416	3417	3417	3418	3419	3419	3420	3421	3421	3422	3423	3423	3424	3425	3425	3426	3427	3427	3428	3429	3429	3430	3431	3431	3432	3432	3433	3434	3434	3435	3436	3436	3437	3438	3438	3439	3440	3440	3441	3442	3442	3443	3443	3444	3445	3445	3446	3447	3447	3448	3449	3449	3450	3451	3451	3452	3452	3453	3454	3454	3455	3456	3456	3457	3458	3458	3459	3459	3460	3461	3461	3462	3463	3463	3464	3465	3465	3466	3466	3467	3468	3468	3469	3470	3470	3471	3471	3472	3473	3473	3474	3475	3475	3476	3476	3477	3478	3478	3479	3480	3480	3481	3481	3482	3483	3483	3484	3485	3485	3486	3486	3487	3488	3488	3489	3489	3490	3491	3491	3492	3493	3493	3494	3494	3495	3496	3496	3497	3497	3498	3499	3499	3500	3500	3501	3502	3502	3503	3503	3504	3505	3505	3506	3506	3507	3508	3508	3509	3510	3510	3511	3511	3512	3513	3513	3514	3514	3515	3516	3516	3517	3517	3518	3518	3519	3520	3520	3521	3521	3522	3523	3523	3524	3524	3525	3526	3526	3527	3527	3528	3529	3529	3530	3530	3531	3532	3532	3533	3533	3534	3534	3535	3536	3536	3537	3537	3538	3539	3539	3540	3540	3541	3541	3542	3543	3543	3544	3544	3545	3546	3546	3547	3547	3548	3548	3549	3550	3550	3551	3551	3552	3552	3553	3554	3554	3555	3555	3556	3556	3557	3558	3558	3559	3559	3560	3560	3561	3562	3562	3563	3563	3564	3564	3565	3566	3566	3567	3567	3568	3568	3569	3569	3570	3571	3571	3572	3572	3573	3573	3574	3575	3575	3576	3576	3577	3577	3578	3578	3579	3580	3580	3581	3581	3582	3582	3583	3583	3584	3585	3585	3586	3586	3587	3587	3588	3588	3589	3589	3590	3591	3591	3592	3592	3593	3593	3594	3594	3595	3596	3596	3597	3597	3598	3598	3599	3599	3600	3600	3601	3602	3602	3603	3603	3604	3604	3605	3605	3606	3606	3607	3607	3608	3609	3609	3610	3610	3611	3611	3612	3612	3613	3613	3614	3614	3615	3615	3616	3617	3617	3618	3618	3619	3619	3620	3620	3621	3621	3622	3622	3623	3623	3624	3624	3625	3626	3626	3627	3627	3628	3628	3629	3629	3630	3630	3631	3631	3632	3632	3633	3633	3634	3634	3635	3635	3636	3636	3637	3638	3638	3639	3639	3640	3640	3641	3641	3642	3642	3643	3643	3644	3644	3645	3645	3646	3646	3647	3647	3648	3648	3649	3649	3650	3650	3651	3651	3652	3652	3653	3653	3654	3654	3655	3655	3656	3656	3657	3657	3658	3658	3659	3659	3660	3660	3661	3661	3662	3662	3663	3663	3664	3664	3665	3665	3666	3666	3667	3667	3668	3668	3669	3669	3670	3670	3671	3671	3672	3672	3673	3673	3674	3674	3675	3675	3676	3676	3677	3677	3678	3678	3679	3679	3680	3680	3681	3681	3682	3682	3683	3683	3684	3684	3685	3685	3686	3686	3687	3687	3688	3688	3689	3689	3689	3690	3690	3691	3691	3692	3692	3693	3693	3694	3694	3695	3695	3696	3696	3697	3697	3698	3698	3699	3699	3700	3700	3700	3701	3701	3702	3702	3703	3703	3704	3704	3705	3705	3706	3706	3707	3707	3708	3708	3709	3709	3709	3710	3710	3711	3711	3712	3712	3713	3713	3714	3714	3715	3715	3716	3716	3716	3717	3717	3718	3718	3719	3719	3720	3720	3721	3721	3722	3722	3722	3723	3723	3724	3724	3725	3725	3726	3726	3727	3727	3727	3728	3728	3729	3729	3730	3730	3731	3731	3732	3732	3732	3733	3733	3734	3734	3735	3735	3736	3736	3737	3737	3737	3738	3738	3739	3739	3740	3740	3741	3741	3741	3742	3742	3743	3743	3744	3744	3745	3745	3745	3746	3746	3747	3747	3748	3748	3749	3749	3749	3750	3750	3751	3751	3752	3752	3752	3753	3753	3754	3754	3755	3755	3756	3756	3756	3757	3757	3758	3758	3759	3759	3759	3760	3760	3761	3761	3762	3762	3762	3763	3763	3764	3764	3765	3765	3765	3766	3766	3767	3767	3768	3768	3768	3769	3769	3770	3770	3771	3771	3771	3772	3772	3773	3773	3774	3774	3774	3775	3775	3776	3776	3776	3777	3777	3778	3778	3779	3779	3779	3780	3780	3781	3781	3781	3782	3782	3783	3783	3784	3784	3784	3785	3785	3786	3786	3786	3787	3787	3788	3788	3789	3789	3789	3790	3790	3791	3791	3791	3792	3792	3793	3793	3793	3794	3794	3795	3795	3795	3796	3796	3797	3797	3797	3798	3798	3799	3799	3800	3800	3800	3801	3801	3802	3802	3802	3803	3803	3804	3804	3804	3805	3805	3806	3806	3806	3807	3807	3808	3808	3808	3809	3809	3809	3810	3810	3811	3811	3811	3812	3812	3813	3813	3813	3814	3814	3815	3815	3815	3816	3816	3817	3817	3817	3818	3818	3818	3819	3819	3820	3820	3820	3821	3821	3822	3822	3822	3823	3823	3824	3824	3824	3825	3825	3825	3826	3826	3827	3827	3827	3828	3828	3828	3829	3829	3830	3830	3830	3831	3831	3832	3832	3832	3833	3833	3833	3834	3834	3835	3835	3835	3836	3836	3836	3837	3837	3838	3838	3838	3839	3839	3839	3840	3840	3840	3841	3841	3842	3842	3842	3843	3843	3843	3844	3844	3845	3845	3845	3846	3846	3846	3847	3847	3847	3848	3848	3849	3849	3849	3850	3850	3850	3851	3851	3851	3852	3852	3853	3853	3853	3854	3854	3854	3855	3855	3855	3856	3856	3857	3857	3857	3858	3858	3858	3859	3859	3859	3860	3860	3860	3861	3861	3862	3862	3862	3863	3863	3863	3864	3864	3864	3865	3865	3865	3866	3866	3866	3867	3867	3867	3868	3868	3869	3869	3869	3870	3870	3870	3871	3871	3871	3872	3872	3872	3873	3873	3873	3874	3874	3874	3875	3875	3875	3876	3876	3876	3877	3877	3877	3878	3878	3878	3879	3879	3880	3880	3880	3881	3881	3881	3882	3882	3882	3883	3883	3883	3884	3884	3884	3885	3885	3885	3886	3886	3886	3887	3887	3887	3888	3888	3888	3889	3889	3889	3890	3890	3890	3891	3891	3891	3892	3892	3892	3893	3893	3893	3893	3894	3894	3894	3895	3895	3895	3896	3896	3896	3897	3897	3897	3898	3898	3898	3899	3899	3899	3900	3900	3900	3901	3901	3901	3902	3902	3902	3903	3903	3903	3903	3904	3904	3904	3905	3905	3905	3906	3906	3906	3907	3907	3907	3908	3908	3908	3909	3909	3909	3909	3910	3910	3910	3911	3911	3911	3912	3912	3912	3913	3913	3913	3914	3914	3914	3914	3915	3915	3915	3916	3916	3916	3917	3917	3917	3917	3918	3918	3918	3919	3919	3919	3920	3920	3920	3921	3921	3921	3921	3922	3922	3922	3923	3923	3923	3924	3924	3924	3924	3925	3925	3925	3926	3926	3926	3927	3927	3927	3927	3928	3928	3928	3929	3929	3929	3929	3930	3930	3930	3931	3931	3931	3932	3932	3932	3932	3933	3933	3933	3934	3934	3934	3934	3935	3935	3935	3936	3936	3936	3936	3937	3937	3937	3938	3938	3938	3938	3939	3939	3939	3940	3940	3940	3940	3941	3941	3941	3942	3942	3942	3942	3943	3943	3943	3944	3944	3944	3944	3945	3945	3945	3946	3946	3946	3946	3947	3947	3947	3947	3948	3948	3948	3949	3949	3949	3949	3950	3950	3950	3951	3951	3951	3951	3952	3952	3952	3952	3953	3953	3953	3954	3954	3954	3954	3955	3955	3955	3955	3956	3956	3956	3956	3957	3957	3957	3958	3958	3958	3958	3959	3959	3959	3959	3960	3960	3960	3960	3961	3961	3961	3962	3962	3962	3962	3963	3963	3963	3963	3964	3964	3964	3964	3965	3965	3965	3965	3966	3966	3966	3966	3967	3967	3967	3967	3968	3968	3968	3969	3969	3969	3969	3970	3970	3970	3970	3971	3971	3971	3971	3972	3972	3972	3972	3973	3973	3973	3973	3974	3974	3974	3974	3975	3975	3975	3975	3976	3976	3976	3976	3977	3977	3977	3977	3978	3978	3978	3978	3979	3979	3979	3979	3979	3980	3980	3980	3980	3981	3981	3981	3981	3982	3982	3982	3982	3983	3983	3983	3983	3984	3984	3984	3984	3985	3985	3985	3985	3985	3986	3986	3986	3986	3987	3987	3987	3987	3988	3988	3988	3988	3989	3989	3989	3989	3989	3990	3990	3990	3990	3991	3991	3991	3991	3992	3992	3992	3992	3992	3993	3993	3993	3993	3994	3994	3994	3994	3995	3995	3995	3995	3995	3996	3996	3996	3996	3997	3997	3997	3997	3997	3998	3998	3998	3998	3999	3999	3999	3999	3999	4000	4000	4000	4000	4001	4001	4001	4001	4001	4002	4002	4002	4002	4003	4003	4003	4003	4003	4004	4004	4004	4004	4004	4005	4005	4005	4005	4006	4006	4006	4006	4006	4007	4007	4007	4007	4007	4008	4008	4008	4008	4009	4009	4009	4009	4009	4010	4010	4010	4010	4010	4011	4011	4011	4011	4011	4012	4012	4012	4012	4012	4013	4013	4013	4013	4013	4014	4014	4014	4014	4015	4015	4015	4015	4015	4016	4016	4016	4016	4016	4017	4017	4017	4017	4017	4018	4018	4018	4018	4018	4019	4019	4019	4019	4019	4019	4020	4020	4020	4020	4020	4021	4021	4021	4021	4021	4022	4022	4022	4022	4022	4023	4023	4023	4023	4023	4024	4024	4024	4024	4024	4024	4025	4025	4025	4025	4025	4026	4026	4026	4026	4026	4027	4027	4027	4027	4027	4027	4028	4028	4028	4028	4028	4029	4029	4029	4029	4029	4030	4030	4030	4030	4030	4030	4031	4031	4031	4031	4031	4032	4032	4032	4032	4032	4032	4033	4033	4033	4033	4033	4033	4034	4034	4034	4034	4034	4035	4035	4035	4035	4035	4035	4036	4036	4036	4036	4036	4036	4037	4037	4037	4037	4037	4037	4038	4038	4038	4038	4038	4038	4039	4039	4039	4039	4039	4039	4040	4040	4040	4040	4040	4040	4041	4041	4041	4041	4041	4041	4042	4042	4042	4042	4042	4042	4043	4043	4043	4043	4043	4043	4044	4044	4044	4044	4044	4044	4045	4045	4045	4045	4045	4045	4046	4046	4046	4046	4046	4046	4046	4047	4047	4047	4047	4047	4047	4048	4048	4048	4048	4048	4048	4048	4049	4049	4049	4049	4049	4049	4050	4050	4050	4050	4050	4050	4050	4051	4051	4051	4051	4051	4051	4052	4052	4052	4052	4052	4052	4052	4053	4053	4053	4053	4053	4053	4053	4054	4054	4054	4054	4054	4054	4054	4055	4055	4055	4055	4055	4055	4055	4056	4056	4056	4056	4056	4056	4056	4057	4057	4057	4057	4057	4057	4057	4058	4058	4058	4058	4058	4058	4058	4058	4059	4059	4059	4059	4059	4059	4059	4060	4060	4060	4060	4060	4060	4060	4061	4061	4061	4061	4061	4061	4061	4061	4062	4062	4062	4062	4062	4062	4062	4062	4063	4063	4063	4063	4063	4063	4063	4063	4064	4064	4064	4064	4064	4064	4064	4065	4065	4065	4065	4065	4065	4065	4065	4065	4066	4066	4066	4066	4066	4066	4066	4066	4067	4067	4067	4067	4067	4067	4067	4067	4068	4068	4068	4068	4068	4068	4068	4068	4068	4069	4069	4069	4069	4069	4069	4069	4069	4070	4070	4070	4070	4070	4070	4070	4070	4070	4071	4071	4071	4071	4071	4071	4071	4071	4071	4072	4072	4072	4072	4072	4072	4072	4072	4072	4073	4073	4073	4073	4073	4073	4073	4073	4073	4073	4074	4074	4074	4074	4074	4074	4074	4074	4074	4075	4075	4075	4075	4075	4075	4075	4075	4075	4075	4076	4076	4076	4076	4076	4076	4076	4076	4076	4076	4077	4077	4077	4077	4077	4077	4077	4077	4077	4077	4077	4078	4078	4078	4078	4078	4078	4078	4078	4078	4078	4079	4079	4079	4079	4079	4079	4079	4079	4079	4079	4079	4080	4080	4080	4080	4080	4080	4080	4080	4080	4080	4080	4080	4081	4081	4081	4081	4081	4081	4081	4081	4081	4081	4081	4082	4082	4082	4082	4082	4082	4082	4082	4082	4082	4082	4082	4083	4083	4083	4083	4083	4083	4083	4083	4083	4083	4083	4083	4083	4084	4084	4084	4084	4084	4084	4084	4084	4084	4084	4084	4084	4084	4085	4085	4085	4085	4085	4085	4085	4085	4085	4085	4085	4085	4085	4086	4086	4086	4086	4086	4086	4086	4086	4086	4086	4086	4086	4086	4086	4086	4087	4087	4087	4087	4087	4087	4087	4087	4087	4087	4087	4087	4087	4087	4087	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4088	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4089	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4090	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4091	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4092	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4093	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4094	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095	4095'
    ccc = ccc.split('	')
    ccc = list(map(int, ccc))
    print(ccc)