--
-- PostgreSQL database dump
--

\restrict yuh7edZbC5MVOCV3cHxvheswluHMiQEAjKshV6qHohjXl7yRyYCohQxbrXehS4d

-- Dumped from database version 14.19 (Homebrew)
-- Dumped by pg_dump version 18.0

-- Started on 2026-06-09 12:37:46 EDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3919 (class 0 OID 20786)
-- Dependencies: 217
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.projects (id, project_name, description, extra_metadata, created_at, updated_at) FROM stdin;
XP00031	12313213132132 Project 6	adsdadsadasd123213213213 asdasdas	"{'lead' : 'no one special'}"	2026-04-08 11:06:26.118308	2026-04-15 11:33:57.733757
XP00033	23132132132131 asdasdsadsad	The creation of the universe	"{'lead': 'adssadasdasdasdasd'}"	2026-04-08 13:24:05.119792	2026-04-15 11:33:57.781983
XP00036	dummy_project123asdsadadsadsad	sadasdsadsa	"{'funding_source': 'Billy'}"	2026-04-13 14:24:57.740201	2026-04-16 11:47:42.345073
XP00035	Microsoft12323213232asdadsadsa	sadadadadsadadsadsadsadsa12313213	"{'funding_source': 'Bill Gates'}"	2026-04-08 13:58:47.039506	2026-04-17 11:12:16.894261
XP00042	PROJ-00006	A project	{"date": "5/5/26", "lead": "Dr. X"}	2026-05-21 11:28:27.34194	2026-05-21 11:28:27.34194
XP00001	PROJ-00001	Project 1	"{'lead': 'Dr. Smith', 'priority': 'high'}"	2026-04-01 16:09:21.152251	2026-04-15 11:03:23.044518
XP00002	PROJ-00002	Project 2	"{'lead': 'Dr. Lee', 'priority': 'medium'}"	2026-04-01 16:09:21.163988	2026-04-15 11:03:23.163013
XP00003	PROJ-00003	Project 3	"{'lead': 'Dr. Chen', 'priority': 'low'}"	2026-04-01 16:09:21.179945	2026-04-15 11:03:23.302713
XP00004	PROJ-00004	Project 4	"{'lead': 'Dr. Patel', 'priority': 'high'}"	2026-04-01 16:09:21.190307	2026-04-15 11:03:23.35279
XP00005	PROJ-00005	Project 5	"{'lead': 'Dr. Gomez', 'priority': 'medium'}"	2026-04-01 16:09:21.197805	2026-04-15 11:03:23.455029
\.


--
-- TOC entry 3920 (class 0 OID 20799)
-- Dependencies: 218
-- Data for Name: samples; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.samples (id, project_id, sample_name, subject_id, status, organism, tissue, extra_metadata, created_at, updated_at) FROM stdin;
XS00001	XP00001	SAMPLE-00001	SUBJ-00001	pending	human	liver	{"age": 45, "tumor_stage": "I"}	2026-04-01 16:09:45.035563	2026-04-01 16:09:45.035563
XS00002	XP00001	SAMPLE-00002	SUBJ-00002	pending	human	lung	{"age": 52, "tumor_stage": "II"}	2026-04-01 16:09:45.071535	2026-04-01 16:09:45.071535
XS00003	XP00001	SAMPLE-00003	SUBJ-00003	complete	mouse	brain	{"age": 12, "tumor_stage": "III"}	2026-04-01 16:09:45.091768	2026-04-01 16:09:45.091768
XS00004	XP00001	SAMPLE-00004	SUBJ-00004	complete	human	kidney	{"age": 60, "tumor_stage": "I"}	2026-04-01 16:09:45.112292	2026-04-01 16:09:45.112292
XS00005	XP00001	SAMPLE-00005	SUBJ-00005	pending	mouse	heart	{"age": 9, "tumor_stage": "II"}	2026-04-01 16:09:45.125833	2026-04-01 16:09:45.125833
XS00006	XP00001	SAMPLE-00006	SUBJ-00006	pending	human	liver	{"age": 50, "tumor_stage": "III"}	2026-04-01 16:09:45.142386	2026-04-01 16:09:45.142386
XS00007	XP00001	SAMPLE-00007	SUBJ-00007	complete	human	lung	{"age": 38, "tumor_stage": "I"}	2026-04-01 16:09:45.152948	2026-04-01 16:09:45.152948
XS00008	XP00001	SAMPLE-00008	SUBJ-00008	complete	mouse	brain	{"age": 15, "tumor_stage": "II"}	2026-04-01 16:09:45.169105	2026-04-01 16:09:45.169105
XS00009	XP00001	SAMPLE-00009	SUBJ-00009	pending	human	kidney	{"age": 42, "tumor_stage": "III"}	2026-04-01 16:09:45.181562	2026-04-01 16:09:45.181562
XS00010	XP00001	SAMPLE-00010	SUBJ-00010	pending	mouse	heart	{"age": 7, "tumor_stage": "I"}	2026-04-01 16:09:45.190876	2026-04-01 16:09:45.190876
XS00011	XP00002	SAMPLE-00011	SUBJ-00011	complete	human	liver	{"age": 55, "tumor_stage": "II"}	2026-04-01 16:09:45.204052	2026-04-01 16:09:45.204052
XS00012	XP00002	SAMPLE-00012	SUBJ-00012	pending	human	lung	{"age": 47, "tumor_stage": "III"}	2026-04-01 16:09:45.221539	2026-04-01 16:09:45.221539
XS00013	XP00002	SAMPLE-00013	SUBJ-00013	pending	mouse	brain	{"age": 14, "tumor_stage": "I"}	2026-04-01 16:09:45.235975	2026-04-01 16:09:45.235975
XS00014	XP00002	SAMPLE-00014	SUBJ-00014	complete	human	kidney	{"age": 63, "tumor_stage": "II"}	2026-04-01 16:09:45.266556	2026-04-01 16:09:45.266556
XS00015	XP00002	SAMPLE-00015	SUBJ-00015	complete	mouse	heart	{"age": 8, "tumor_stage": "III"}	2026-04-01 16:09:45.281608	2026-04-01 16:09:45.281608
XS00016	XP00002	SAMPLE-00016	SUBJ-00016	pending	human	liver	{"age": 39, "tumor_stage": "I"}	2026-04-01 16:09:45.293172	2026-04-01 16:09:45.293172
XS00017	XP00002	SAMPLE-00017	SUBJ-00017	pending	human	lung	{"age": 50, "tumor_stage": "II"}	2026-04-01 16:09:45.305407	2026-04-01 16:09:45.305407
XS00018	XP00002	SAMPLE-00018	SUBJ-00018	complete	mouse	brain	{"age": 13, "tumor_stage": "III"}	2026-04-01 16:09:45.315006	2026-04-01 16:09:45.315006
XS00019	XP00002	SAMPLE-00019	SUBJ-00019	complete	human	kidney	{"age": 46, "tumor_stage": "I"}	2026-04-01 16:09:45.330984	2026-04-01 16:09:45.330984
XS00020	XP00002	SAMPLE-00020	SUBJ-00020	pending	mouse	heart	{"age": 10, "tumor_stage": "II"}	2026-04-01 16:09:45.341374	2026-04-01 16:09:45.341374
XS00021	XP00003	SAMPLE-00021	SUBJ-00021	pending	human	liver	{"age": 53, "tumor_stage": "III"}	2026-04-01 16:09:45.359851	2026-04-01 16:09:45.359851
XS00022	XP00003	SAMPLE-00022	SUBJ-00022	complete	human	lung	{"age": 48, "tumor_stage": "I"}	2026-04-01 16:09:45.371409	2026-04-01 16:09:45.371409
XS00023	XP00003	SAMPLE-00023	SUBJ-00023	complete	mouse	brain	{"age": 16, "tumor_stage": "II"}	2026-04-01 16:09:45.383708	2026-04-01 16:09:45.383708
XS00024	XP00003	SAMPLE-00024	SUBJ-00024	pending	human	kidney	{"age": 61, "tumor_stage": "III"}	2026-04-01 16:09:45.3927	2026-04-01 16:09:45.3927
XS00025	XP00003	SAMPLE-00025	SUBJ-00025	pending	mouse	heart	{"age": 11, "tumor_stage": "I"}	2026-04-01 16:09:45.408547	2026-04-01 16:09:45.408547
XS00026	XP00003	SAMPLE-00026	SUBJ-00026	complete	human	liver	{"age": 49, "tumor_stage": "II"}	2026-04-01 16:09:45.416288	2026-04-01 16:09:45.416288
XS00027	XP00003	SAMPLE-00027	SUBJ-00027	complete	human	lung	{"age": 51, "tumor_stage": "III"}	2026-04-01 16:09:45.42679	2026-04-01 16:09:45.42679
XS00028	XP00003	SAMPLE-00028	SUBJ-00028	pending	mouse	brain	{"age": 15, "tumor_stage": "I"}	2026-04-01 16:09:45.434227	2026-04-01 16:09:45.434227
XS00029	XP00003	SAMPLE-00029	SUBJ-00029	pending	human	kidney	{"age": 44, "tumor_stage": "II"}	2026-04-01 16:09:45.442023	2026-04-01 16:09:45.442023
XS00030	XP00003	SAMPLE-00030	SUBJ-00030	complete	mouse	heart	{"age": 12, "tumor_stage": "III"}	2026-04-01 16:09:45.452752	2026-04-01 16:09:45.452752
XS00031	XP00004	SAMPLE-00031	SUBJ-00031	pending	human	liver	{"age": 42, "tumor_stage": "I"}	2026-04-01 16:09:45.461499	2026-04-01 16:09:45.461499
XS00032	XP00004	SAMPLE-00032	SUBJ-00032	complete	human	lung	{"age": 55, "tumor_stage": "II"}	2026-04-01 16:09:45.469445	2026-04-01 16:09:45.469445
XS00033	XP00004	SAMPLE-00033	SUBJ-00033	complete	mouse	brain	{"age": 14, "tumor_stage": "III"}	2026-04-01 16:09:45.482299	2026-04-01 16:09:45.482299
XS00034	XP00004	SAMPLE-00034	SUBJ-00034	pending	human	kidney	{"age": 59, "tumor_stage": "I"}	2026-04-01 16:09:45.48995	2026-04-01 16:09:45.48995
XS00035	XP00004	SAMPLE-00035	SUBJ-00035	pending	mouse	heart	{"age": 13, "tumor_stage": "II"}	2026-04-01 16:09:45.498398	2026-04-01 16:09:45.498398
XS00036	XP00004	SAMPLE-00036	SUBJ-00036	complete	human	liver	{"age": 50, "tumor_stage": "III"}	2026-04-01 16:09:45.513021	2026-04-01 16:09:45.513021
XS00037	XP00004	SAMPLE-00037	SUBJ-00037	complete	human	lung	{"age": 45, "tumor_stage": "I"}	2026-04-01 16:09:45.521847	2026-04-01 16:09:45.521847
XS00038	XP00004	SAMPLE-00038	SUBJ-00038	pending	mouse	brain	{"age": 17, "tumor_stage": "II"}	2026-04-01 16:09:45.534177	2026-04-01 16:09:45.534177
XS00039	XP00004	SAMPLE-00039	SUBJ-00039	pending	human	kidney	{"age": 48, "tumor_stage": "III"}	2026-04-01 16:09:45.543229	2026-04-01 16:09:45.543229
XS00040	XP00004	SAMPLE-00040	SUBJ-00040	complete	mouse	heart	{"age": 12, "tumor_stage": "I"}	2026-04-01 16:09:45.55151	2026-04-01 16:09:45.55151
XS00041	XP00005	SAMPLE-00041	SUBJ-00041	pending	human	liver	{"age": 51, "tumor_stage": "II"}	2026-04-01 16:09:45.562542	2026-04-01 16:09:45.562542
XS00042	XP00005	SAMPLE-00042	SUBJ-00042	complete	human	lung	{"age": 49, "tumor_stage": "III"}	2026-04-01 16:09:45.574099	2026-04-01 16:09:45.574099
XS00043	XP00005	SAMPLE-00043	SUBJ-00043	complete	mouse	brain	{"age": 16, "tumor_stage": "I"}	2026-04-01 16:09:45.587877	2026-04-01 16:09:45.587877
XS00044	XP00005	SAMPLE-00044	SUBJ-00044	pending	human	kidney	{"age": 57, "tumor_stage": "II"}	2026-04-01 16:09:45.599846	2026-04-01 16:09:45.599846
XS00045	XP00005	SAMPLE-00045	SUBJ-00045	pending	mouse	heart	{"age": 10, "tumor_stage": "III"}	2026-04-01 16:09:45.608375	2026-04-01 16:09:45.608375
XS00046	XP00005	SAMPLE-00046	SUBJ-00046	complete	human	liver	{"age": 46, "tumor_stage": "I"}	2026-04-01 16:09:45.623987	2026-04-01 16:09:45.623987
XS00047	XP00005	SAMPLE-00047	SUBJ-00047	complete	human	lung	{"age": 52, "tumor_stage": "II"}	2026-04-01 16:09:45.634313	2026-04-01 16:09:45.634313
XS00048	XP00005	SAMPLE-00048	SUBJ-00048	pending	mouse	brain	{"age": 15, "tumor_stage": "III"}	2026-04-01 16:09:45.649793	2026-04-01 16:09:45.649793
XS00049	XP00005	SAMPLE-00049	SUBJ-00049	pending	human	kidney	{"age": 47, "tumor_stage": "I"}	2026-04-01 16:09:45.6701	2026-04-01 16:09:45.6701
XS00050	XP00005	SAMPLE-00050	SUBJ-00050	complete	mouse	heart	{"age": 11, "tumor_stage": "II"}	2026-04-01 16:09:45.684539	2026-04-01 16:09:45.684539
\.


--
-- TOC entry 3921 (class 0 OID 20816)
-- Dependencies: 219
-- Data for Name: experiments; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.experiments (id, sample_id, assay_type, library_prep_date, library_protocol, library_version, extra_metadata, created_at, updated_at) FROM stdin;
XE00050	XS00049	ATAC-Seq	2026-04-19	Omni-ATAC	v1	"{'kit': 'Kit-B', 'operator': 'Eve', 'tumor_stage': 'II'}"	2026-04-01 16:11:57.096761	2026-04-23 14:36:11.139925
XE00049	XS00049	RNA-Seq	2026-04-18	PolyA	v2	"{'kit': 'Kit-A', 'operator': 'Dan', 'tumor_stage': 'I'}"	2026-04-01 16:11:57.077134	2026-04-23 14:36:11.221112
XE00048	XS00048	ChIP-Seq	2026-04-17	ChIPmentation	v1	"{'kit': 'Kit-C', 'operator': 'Carol', 'tumor_stage': 'III'}"	2026-04-01 16:11:57.065245	2026-04-23 14:36:11.2782
XE00047	XS00047	RNA-Seq	2026-04-16	RiboMinus	v1	"{'kit': 'Kit-B', 'operator': 'Bob', 'tumor_stage': 'II'}"	2026-04-01 16:11:57.047133	2026-04-23 14:36:11.331019
XE00046	XS00046	ATAC-Seq	2026-04-15	Omni-ATAC	v2	"{'kit': 'Kit-A', 'operator': 'Alice', 'tumor_stage': 'I'}"	2026-04-01 16:11:57.033454	2026-04-23 14:36:11.403057
XE00045	XS00045	ATAC-Seq	2026-04-14	Omni-ATAC	v1	"{'kit': 'Kit-C', 'operator': 'Eve', 'tumor_stage': 'III'}"	2026-04-01 16:11:57.020304	2026-04-23 14:36:11.463573
XE00044	XS00044	ChIP-Seq	2026-04-13	ChIPmentation	v2	"{'kit': 'Kit-B', 'operator': 'Dan', 'tumor_stage': 'II'}"	2026-04-01 16:11:57.011675	2026-04-23 14:36:11.517882
XE00043	XS00043	ChIP-Seq	2026-04-12	ChIPmentation	v1	"{'kit': 'Kit-A', 'operator': 'Carol', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.99861	2026-04-23 14:36:11.599922
XE00042	XS00042	RNA-Seq	2026-04-11	RiboMinus	v2	"{'kit': 'Kit-C', 'operator': 'Bob', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.987658	2026-04-23 14:36:11.637997
XE00041	XS00041	RNA-Seq	2026-04-10	PolyA	v1	"{'kit': 'Kit-B', 'operator': 'Alice', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.972888	2026-04-23 14:36:11.695955
XE00040	XS00040	ATAC-Seq	2026-04-09	Omni-ATAC	v1	"{'kit': 'Kit-A', 'operator': 'Eve', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.942624	2026-04-23 14:36:11.791875
XE00039	XS00039	RNA-Seq	2026-04-08	PolyA	v2	"{'kit': 'Kit-C', 'operator': 'Dan', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.927488	2026-04-23 14:36:11.854
XE00038	XS00038	ChIP-Seq	2026-04-07	ChIPmentation	v1	"{'kit': 'Kit-B', 'operator': 'Carol', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.917326	2026-04-23 14:36:11.911008
XE00037	XS00037	RNA-Seq	2026-04-06	RiboMinus	v1	"{'kit': 'Kit-A', 'operator': 'Bob', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.904307	2026-04-23 14:36:11.9864
XE00036	XS00036	ATAC-Seq	2026-04-05	Omni-ATAC	v2	"{'kit': 'Kit-C', 'operator': 'Alice', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.89284	2026-04-23 14:36:12.073912
XE00035	XS00035	ATAC-Seq	2026-04-04	Omni-ATAC	v1	"{'kit': 'Kit-B', 'operator': 'Eve', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.882946	2026-04-23 14:36:12.189622
XE00034	XS00034	ChIP-Seq	2026-04-03	ChIPmentation	v2	"{'kit': 'Kit-A', 'operator': 'Dan', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.869018	2026-04-23 14:36:12.29456
XE00033	XS00033	ChIP-Seq	2026-04-02	ChIPmentation	v1	"{'kit': 'Kit-C', 'operator': 'Carol', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.860291	2026-04-23 14:36:12.414167
XE00032	XS00032	RNA-Seq	2026-04-01	RiboMinus	v2	"{'kit': 'Kit-B', 'operator': 'Bob', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.851381	2026-04-23 14:36:12.512759
XE00031	XS00031	RNA-Seq	2026-03-31	PolyA	v1	"{'kit': 'Kit-A', 'operator': 'Alice', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.829833	2026-04-23 14:36:12.604857
XE00030	XS00030	ATAC-Seq	2026-03-30	Omni-ATAC	v1	"{'kit': 'Kit-C', 'operator': 'Eve', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.814319	2026-04-23 14:36:12.693356
XE00029	XS00029	RNA-Seq	2026-03-29	PolyA	v2	"{'kit': 'Kit-B', 'operator': 'Dan', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.805108	2026-04-23 14:36:12.77955
XE00028	XS00028	ChIP-Seq	2026-03-28	ChIPmentation	v1	"{'kit': 'Kit-A', 'operator': 'Carol', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.792384	2026-04-23 14:36:12.838922
XE00027	XS00027	RNA-Seq	2026-03-27	RiboMinus	v1	"{'kit': 'Kit-C', 'operator': 'Bob', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.781576	2026-04-23 14:36:12.903118
XE00026	XS00026	ATAC-Seq	2026-03-26	Omni-ATAC	v2	"{'kit': 'Kit-B', 'operator': 'Alice', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.771752	2026-04-23 14:36:12.948125
XE00025	XS00025	ATAC-Seq	2026-03-25	Omni-ATAC	v1	"{'kit': 'Kit-A', 'operator': 'Eve', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.757271	2026-04-23 14:36:13.019036
XE00024	XS00024	ChIP-Seq	2026-03-24	ChIPmentation	v2	"{'kit': 'Kit-C', 'operator': 'Dan', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.742074	2026-04-23 14:36:13.075833
XE00023	XS00023	ChIP-Seq	2026-03-23	ChIPmentation	v1	"{'kit': 'Kit-B', 'operator': 'Carol', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.729021	2026-04-23 14:36:13.148238
XE00022	XS00022	RNA-Seq	2026-03-22	RiboMinus	v2	"{'kit': 'Kit-A', 'operator': 'Bob', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.716015	2026-04-23 14:36:13.238111
XE00021	XS00021	RNA-Seq	2026-03-21	PolyA	v1	"{'kit': 'Kit-C', 'operator': 'Alice', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.700671	2026-04-23 14:36:13.327068
XE00020	XS00020	ATAC-Seq	2026-03-20	Omni-ATAC	v1	"{'kit': 'Kit-B', 'operator': 'Eve', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.69109	2026-04-23 14:36:13.399749
XE00019	XS00019	RNA-Seq	2026-03-19	PolyA	v2	"{'kit': 'Kit-A', 'operator': 'Dan', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.678826	2026-04-23 14:36:13.459671
XE00018	XS00018	ChIP-Seq	2026-03-18	ChIPmentation	v1	"{'kit': 'Kit-C', 'operator': 'Carol', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.661761	2026-04-23 14:36:13.519739
XE00017	XS00017	RNA-Seq	2026-03-17	RiboMinus	v1	"{'kit': 'Kit-B', 'operator': 'Bob', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.652809	2026-04-23 14:36:13.608201
XE00016	XS00016	ATAC-Seq	2026-03-16	Omni-ATAC	v2	"{'kit': 'Kit-A', 'operator': 'Alice', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.642282	2026-04-23 14:36:13.664608
XE00015	XS00015	ATAC-Seq	2026-03-15	Omni-ATAC	v1	"{'kit': 'Kit-C', 'operator': 'Eve', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.633249	2026-04-23 14:36:13.725752
XE00014	XS00014	ChIP-Seq	2026-03-14	ChIPmentation	v2	"{'kit': 'Kit-B', 'operator': 'Dan', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.618337	2026-04-23 14:36:13.78069
XE00013	XS00013	ChIP-Seq	2026-03-13	ChIPmentation	v1	"{'kit': 'Kit-A', 'operator': 'Carol', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.599898	2026-04-23 14:36:13.86069
XE00012	XS00012	RNA-Seq	2026-03-12	RiboMinus	v2	"{'kit': 'Kit-C', 'operator': 'Bob', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.587194	2026-04-23 14:36:13.921123
XE00011	XS00011	RNA-Seq	2026-03-11	PolyA	v1	"{'kit': 'Kit-B', 'operator': 'Alice', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.572181	2026-04-23 14:36:13.990861
XE00010	XS00010	ATAC-Seq	2026-03-10	Omni-ATAC	v1	"{'kit': 'Kit-A', 'operator': 'Eve', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.558225	2026-04-23 14:36:14.056346
XE00009	XS00009	RNA-Seq	2026-03-09	PolyA	v2	"{'kit': 'Kit-C', 'operator': 'Dan', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.549279	2026-04-23 14:36:14.120442
XE00008	XS00008	ChIP-Seq	2026-03-08	ChIPmentation	v1	"{'kit': 'Kit-B', 'operator': 'Carol', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.538092	2026-04-23 14:36:14.18732
XE00007	XS00007	RNA-Seq	2026-03-07	RiboMinus	v1	"{'kit': 'Kit-A', 'operator': 'Bob', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.523659	2026-04-23 14:36:14.253798
XE00006	XS00006	ATAC-Seq	2026-03-06	Omni-ATAC	v2	"{'kit': 'Kit-C', 'operator': 'Alice', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.510661	2026-04-23 14:36:14.326656
XE00005	XS00005	ATAC-Seq	2026-03-05	Omni-ATAC	v1	"{'kit': 'Kit-B', 'operator': 'Eve', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.494795	2026-04-23 14:36:14.40701
XE00004	XS00004	ChIP-Seq	2026-03-04	ChIPmentation	v2	"{'kit': 'Kit-A', 'operator': 'Dan', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.475052	2026-04-23 14:36:14.475531
XE00002	XS00002	RNA-Seq	2026-03-02	PolyA	v2	"{'kit': 'Kit-B', 'operator': 'Bob', 'tumor_stage': 'II'}"	2026-04-01 16:11:56.440162	2026-04-23 14:36:14.640831
XE00001	XS00001	RNA-Seq	2026-03-01	PolyA	v1	"{'kit': 'Kit-A', 'operator': 'Alice', 'tumor_stage': 'I'}"	2026-04-01 16:11:56.410498	2026-04-23 14:36:14.711269
XE00003	XS00003	ChIP-Seq	2026-03-03	ChIPmentation	v1	"{'kit': 'Kit-C', 'operator': 'Carol', 'tumor_stage': 'III'}"	2026-04-01 16:11:56.457935	2026-04-23 14:36:14.546258
\.


--
-- TOC entry 3922 (class 0 OID 20831)
-- Dependencies: 220
-- Data for Name: sequencing_runs; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.sequencing_runs (id, flowcell_id, machine, run_date, read_length, sequencing_center, extra_metadata, created_at) FROM stdin;
XR00001	FC-00001	NovaSeq6000	2026-03-15	150	Broad Institute	{"extra_metadata": "{\\"operator\\": \\"Alice\\", \\"kit_version\\": \\"v2\\"}"}	2026-04-02 14:02:53.862647
XR00002	FC-00002	NextSeq2000	2026-03-16	100	MGH Genomics	{"extra_metadata": "{\\"operator\\": \\"Bob\\"}"}	2026-04-02 14:02:53.899011
XR00003	FC-00003	NovaSeq6000	2026-03-17	150	Stanford Genomics	{"extra_metadata": "{\\"operator\\": \\"Carol\\", \\"notes\\": \\"high yield\\"}"}	2026-04-02 14:02:53.925714
XR00004	FC-00004	NextSeq2000	2026-03-18	75	Broad Institute	{"extra_metadata": "{\\"operator\\": \\"Alice\\", \\"kit_version\\": \\"v1\\"}"}	2026-04-02 14:02:53.941716
XR00005	FC-00005	NovaSeq6000	2026-03-19	150	MGH Genomics	{"extra_metadata": "{\\"operator\\": \\"Bob\\", \\"notes\\": \\"low cluster density\\"}"}	2026-04-02 14:02:53.962563
\.


--
-- TOC entry 3923 (class 0 OID 20844)
-- Dependencies: 221
-- Data for Name: run_experiments; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.run_experiments (id, experiment_id, run_id, lane, index_sequence, created_at, extra_metadata, updated_at) FROM stdin;
XER00050	XE00050	XR00004	4	AACCGG	2026-04-02 15:51:48.76224	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:07.465849
XER00049	XE00049	XR00004	3	CGATGT	2026-04-02 15:51:48.740883	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:07.517715
XER00048	XE00048	XR00003	3	TTGGCA	2026-04-02 15:51:48.727359	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:07.570563
XER00047	XE00047	XR00002	2	GCTAAC	2026-04-02 15:51:48.717187	"{'extra_metadata': '{\\"pool\\": \\"J\\"}'}"	2026-04-23 15:40:07.677783
XER00046	XE00046	XR00001	2	ATCGTG	2026-04-02 15:51:48.702857	"{'extra_metadata': '{\\"pool\\": \\"J\\"}'}"	2026-04-23 15:40:07.748425
XER00045	XE00045	XR00005	3	AACCGG	2026-04-02 15:51:48.689836	"{'extra_metadata': '{\\"qc\\": \\"fail\\"}'}"	2026-04-23 15:40:07.813848
XER00044	XE00044	XR00004	2	CGATGT	2026-04-02 15:51:48.678411	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:07.907933
XER00043	XE00043	XR00003	2	TTGGCA	2026-04-02 15:51:48.657942	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:07.982431
XER00042	XE00042	XR00002	1	GCTAAC	2026-04-02 15:51:48.648308	"{'extra_metadata': '{\\"pool\\": \\"I\\"}'}"	2026-04-23 15:40:08.08229
XER00041	XE00041	XR00001	1	ATCGTG	2026-04-02 15:51:48.637191	"{'extra_metadata': '{\\"pool\\": \\"I\\"}'}"	2026-04-23 15:40:08.181306
XER00040	XE00040	XR00005	2	AACCGG	2026-04-02 15:51:48.624264	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:08.268939
XER00039	XE00039	XR00004	1	CGATGT	2026-04-02 15:51:48.614543	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:08.355012
XER00038	XE00038	XR00003	1	TTGGCA	2026-04-02 15:51:48.597986	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:08.44702
XER00037	XE00037	XR00002	4	GCTAAC	2026-04-02 15:51:48.584975	"{'extra_metadata': '{\\"pool\\": \\"H\\"}'}"	2026-04-23 15:40:08.539927
XER00036	XE00036	XR00001	4	ATCGTG	2026-04-02 15:51:48.570429	"{'extra_metadata': '{\\"pool\\": \\"H\\"}'}"	2026-04-23 15:40:08.61081
XER00035	XE00035	XR00005	1	AACCGG	2026-04-02 15:51:48.555502	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:08.68079
XER00034	XE00034	XR00004	4	CGATGT	2026-04-02 15:51:48.544535	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:08.764401
XER00033	XE00033	XR00003	4	TTGGCA	2026-04-02 15:51:48.530867	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:08.838594
XER00032	XE00032	XR00002	3	GCTAAC	2026-04-02 15:51:48.513689	"{'extra_metadata': '{\\"pool\\": \\"G\\"}'}"	2026-04-23 15:40:08.915269
XER00031	XE00031	XR00001	3	ATCGTG	2026-04-02 15:51:48.498749	"{'extra_metadata': '{\\"pool\\": \\"G\\"}'}"	2026-04-23 15:40:08.98228
XER00030	XE00030	XR00005	4	AACCGG	2026-04-02 15:51:48.484205	"{'extra_metadata': '{\\"qc\\": \\"fail\\"}'}"	2026-04-23 15:40:09.051537
XER00029	XE00029	XR00004	3	CGATGT	2026-04-02 15:51:48.471142	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:09.125372
XER00028	XE00028	XR00003	3	TTGGCA	2026-04-02 15:51:48.45768	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:09.21823
XER00027	XE00027	XR00002	2	GCTAAC	2026-04-02 15:51:48.446109	"{'extra_metadata': '{\\"pool\\": \\"F\\"}'}"	2026-04-23 15:40:09.330818
XER00026	XE00026	XR00001	2	ATCGTG	2026-04-02 15:51:48.432214	"{'extra_metadata': '{\\"pool\\": \\"F\\"}'}"	2026-04-23 15:40:09.40458
XER00025	XE00025	XR00005	3	AACCGG	2026-04-02 15:51:48.419387	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:09.482102
XER00024	XE00024	XR00004	2	CGATGT	2026-04-02 15:51:48.41016	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:09.579629
XER00023	XE00023	XR00003	2	TTGGCA	2026-04-02 15:51:48.392961	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:09.669888
XER00022	XE00022	XR00002	1	GCTAAC	2026-04-02 15:51:48.38026	"{'extra_metadata': '{\\"pool\\": \\"E\\"}'}"	2026-04-23 15:40:09.756787
XER00021	XE00021	XR00001	1	ATCGTG	2026-04-02 15:51:48.371208	"{'extra_metadata': '{\\"pool\\": \\"E\\"}'}"	2026-04-23 15:40:09.846201
XER00020	XE00020	XR00005	2	AACCGG	2026-04-02 15:51:48.362395	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:09.946991
XER00019	XE00019	XR00004	1	CGATGT	2026-04-02 15:51:48.353488	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:10.034837
XER00018	XE00018	XR00003	1	TTGGCA	2026-04-02 15:51:48.343974	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:10.118026
XER00017	XE00017	XR00002	4	GCTAAC	2026-04-02 15:51:48.334325	"{'extra_metadata': '{\\"pool\\": \\"D\\"}'}"	2026-04-23 15:40:10.187628
XER00016	XE00016	XR00001	4	ATCGTG	2026-04-02 15:51:48.324999	"{'extra_metadata': '{\\"pool\\": \\"D\\"}'}"	2026-04-23 15:40:10.253505
XER00015	XE00015	XR00005	1	AACCGG	2026-04-02 15:51:48.313431	"{'extra_metadata': '{\\"qc\\": \\"fail\\"}'}"	2026-04-23 15:40:10.347186
XER00014	XE00014	XR00004	4	CGATGT	2026-04-02 15:51:48.303672	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:10.438248
XER00013	XE00013	XR00003	4	TTGGCA	2026-04-02 15:51:48.291953	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:10.521499
XER00012	XE00012	XR00002	3	GCTAAC	2026-04-02 15:51:48.282362	"{'extra_metadata': '{\\"pool\\": \\"C\\"}'}"	2026-04-23 15:40:10.617111
XER00011	XE00011	XR00001	3	ATCGTG	2026-04-02 15:51:48.264629	"{'extra_metadata': '{\\"pool\\": \\"C\\"}'}"	2026-04-23 15:40:10.705931
XER00010	XE00010	XR00005	4	AACCGG	2026-04-02 15:51:48.250798	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:10.775233
XER00009	XE00009	XR00004	3	CGATGT	2026-04-02 15:51:48.23988	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:10.858422
XER00008	XE00008	XR00003	3	TTGGCA	2026-04-02 15:51:48.221876	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:10.958596
XER00007	XE00007	XR00002	2	GCTAAC	2026-04-02 15:51:48.207988	"{'extra_metadata': '{\\"pool\\": \\"B\\"}'}"	2026-04-23 15:40:11.01453
XER00006	XE00006	XR00001	2	ATCGTG	2026-04-02 15:51:48.199379	"{'extra_metadata': '{\\"pool\\": \\"B\\"}'}"	2026-04-23 15:40:11.096135
XER00005	XE00005	XR00005	3	AACCGG	2026-04-02 15:51:48.184647	"{'extra_metadata': '{\\"qc\\": \\"pass\\"}'}"	2026-04-23 15:40:11.222307
XER00004	XE00004	XR00004	2	CGATGT	2026-04-02 15:51:48.173903	"{'extra_metadata': '{\\"antibody\\": \\"H3K4me3\\"}'}"	2026-04-23 15:40:11.344447
XER00003	XE00003	XR00003	2	TTGGCA	2026-04-02 15:51:48.14737	"{'extra_metadata': '{\\"antibody\\": \\"H3K27ac\\"}'}"	2026-04-23 15:40:11.436257
XER00002	XE00002	XR00002	1	GCTAAC	2026-04-02 15:51:48.116168	"{'extra_metadata': '{\\"pool\\": \\"A\\"}'}"	2026-04-23 15:40:11.511447
XER00001	XE00001	XR00001	1	ATCGTG	2026-04-02 15:51:48.021275	"{'extra_metadata': '{\\"pool\\": \\"A\\"}'}"	2026-04-23 15:40:11.583895
\.


--
-- TOC entry 3930 (class 0 OID 20951)
-- Dependencies: 228
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.files (id, gcs_uri, gcs_bucket, file_path, file_type, file_format, size_bytes, checksum_md5, run_experiment_id, experiment_id, extra_metadata, created_at, updated_at) FROM stdin;
XF00232	gs://lims-analysis/atac_seq/SAMPLE-00030/2026-03-30/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00030	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:52.923045	2026-04-07 13:06:52.923045
XF00236	gs://lims-analysis/atac_seq/SAMPLE-00040/2026-04-09/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00040	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:54.103837	2026-04-07 13:06:54.103837
XF00240	gs://lims-analysis/atac_seq/SAMPLE-00050/2026-04-19/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00050	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:55.248421	2026-04-07 13:06:55.248421
XF00516	gs://lims-analysis/chip_seq/SAMPLE-00028/2026-03-28/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00028	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:54.68049	2026-04-07 14:00:54.68049
XF00526	gs://lims-analysis/chip_seq/SAMPLE-00033/2026-04-02/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00033	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:56.7623	2026-04-07 14:00:56.7623
XF00536	gs://lims-analysis/chip_seq/SAMPLE-00038/2026-04-07/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00038	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:59.461553	2026-04-07 14:00:59.461553
XF00546	gs://lims-analysis/chip_seq/SAMPLE-00043/2026-04-12/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00043	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:03.188362	2026-04-07 14:01:03.188362
XF00556	gs://lims-analysis/chip_seq/SAMPLE-00048/2026-04-17/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00048	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:05.269936	2026-04-07 14:01:05.269936
XF00464	gs://lims-analysis/rna_seq/SAMPLE-00002/2026-03-02/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00002	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:41.089331	2026-04-07 14:00:41.089331
XF00467	gs://lims-analysis/chip_seq/SAMPLE-00004/2026-03-04/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00004	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:42.824329	2026-04-07 14:00:42.824329
XF00473	gs://lims-analysis/rna_seq/SAMPLE-00007/2026-03-07/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00007	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:43.874872	2026-04-07 14:00:43.874872
XF00476	gs://lims-analysis/chip_seq/SAMPLE-00008/2026-03-08/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00008	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:44.31878	2026-04-07 14:00:44.31878
XF00479	gs://lims-analysis/atac_seq/SAMPLE-00010/2026-03-10/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00010	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:44.704337	2026-04-07 14:00:44.704337
XF00482	gs://lims-analysis/rna_seq/SAMPLE-00011/2026-03-11/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00011	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:46.366608	2026-04-07 14:00:46.366608
XF00484	gs://lims-analysis/rna_seq/SAMPLE-00012/2026-03-12/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00012	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:46.707401	2026-04-07 14:00:46.707401
XF00486	gs://lims-analysis/chip_seq/SAMPLE-00013/2026-03-13/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00013	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:46.978914	2026-04-07 14:00:46.978914
XF00488	gs://lims-analysis/chip_seq/SAMPLE-00014/2026-03-14/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00014	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:47.330777	2026-04-07 14:00:47.330777
XF00492	gs://lims-analysis/atac_seq/SAMPLE-00016/2026-03-16/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00016	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:48.834396	2026-04-07 14:00:48.834396
XF00494	gs://lims-analysis/rna_seq/SAMPLE-00017/2026-03-17/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00017	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:49.101738	2026-04-07 14:00:49.101738
XF00233	gs://lims-analysis/rna_seq/SAMPLE-00031/2026-03-31/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00031	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:52.974927	2026-04-07 13:06:52.974927
XF00237	gs://lims-analysis/rna_seq/SAMPLE-00041/2026-04-10/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00041	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:54.15948	2026-04-07 13:06:54.15948
XF00512	gs://lims-analysis/atac_seq/SAMPLE-00026/2026-03-26/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00026	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:53.60192	2026-04-07 14:00:53.60192
XF00517	gs://lims-analysis/rna_seq/SAMPLE-00029/2026-03-29/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00029	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:54.86067	2026-04-07 14:00:54.86067
XF00522	gs://lims-analysis/rna_seq/SAMPLE-00031/2026-03-31/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00031	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:56.056698	2026-04-07 14:00:56.056698
XF00527	gs://lims-analysis/chip_seq/SAMPLE-00034/2026-04-03/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00034	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:56.895698	2026-04-07 14:00:56.895698
XF00532	gs://lims-analysis/atac_seq/SAMPLE-00036/2026-04-05/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00036	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:57.687093	2026-04-07 14:00:57.687093
XF00537	gs://lims-analysis/rna_seq/SAMPLE-00039/2026-04-08/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00039	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:59.604575	2026-04-07 14:00:59.604575
XF00542	gs://lims-analysis/rna_seq/SAMPLE-00041/2026-04-10/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00041	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:01.646608	2026-04-07 14:01:01.646608
XF00547	gs://lims-analysis/chip_seq/SAMPLE-00044/2026-04-13/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00044	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:03.347961	2026-04-07 14:01:03.347961
XF00552	gs://lims-analysis/atac_seq/SAMPLE-00046/2026-04-15/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00046	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:04.69148	2026-04-07 14:01:04.69148
XF00557	gs://lims-analysis/rna_seq/SAMPLE-00049/2026-04-18/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00049	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:05.479554	2026-04-07 14:01:05.479554
XF00462	gs://lims-analysis/rna_seq/SAMPLE-00001/2026-03-01/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00001	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:40.284588	2026-04-07 14:00:40.284588
XF00465	gs://lims-analysis/chip_seq/SAMPLE-00003/2026-03-03/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00003	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:42.204831	2026-04-07 14:00:42.204831
XF00468	gs://lims-analysis/chip_seq/SAMPLE-00004/2026-03-04/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00004	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:42.970805	2026-04-07 14:00:42.970805
XF00474	gs://lims-analysis/rna_seq/SAMPLE-00007/2026-03-07/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00007	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:44.029941	2026-04-07 14:00:44.029941
XF00477	gs://lims-analysis/rna_seq/SAMPLE-00009/2026-03-09/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00009	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:44.436646	2026-04-07 14:00:44.436646
XF00483	gs://lims-analysis/rna_seq/SAMPLE-00012/2026-03-12/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00012	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:46.47835	2026-04-07 14:00:46.47835
XF00485	gs://lims-analysis/chip_seq/SAMPLE-00013/2026-03-13/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00013	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:46.849641	2026-04-07 14:00:46.849641
XF00487	gs://lims-analysis/chip_seq/SAMPLE-00014/2026-03-14/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00014	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:47.149266	2026-04-07 14:00:47.149266
XF00489	gs://lims-analysis/atac_seq/SAMPLE-00015/2026-03-15/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00015	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:48.274725	2026-04-07 14:00:48.274725
XF00493	gs://lims-analysis/rna_seq/SAMPLE-00017/2026-03-17/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00017	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:48.985417	2026-04-07 14:00:48.985417
XF00495	gs://lims-analysis/chip_seq/SAMPLE-00018/2026-03-18/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00018	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:49.258809	2026-04-07 14:00:49.258809
XF00496	gs://lims-analysis/chip_seq/SAMPLE-00018/2026-03-18/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00018	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:49.403054	2026-04-07 14:00:49.403054
XF00497	gs://lims-analysis/rna_seq/SAMPLE-00019/2026-03-19/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00019	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:49.562595	2026-04-07 14:00:49.562595
XF00234	gs://lims-analysis/atac_seq/SAMPLE-00035/2026-04-04/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00035	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:53.505023	2026-04-07 13:06:53.505023
XF00238	gs://lims-analysis/atac_seq/SAMPLE-00045/2026-04-14/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00045	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:54.678559	2026-04-07 13:06:54.678559
XF00513	gs://lims-analysis/rna_seq/SAMPLE-00027/2026-03-27/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00027	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:53.756914	2026-04-07 14:00:53.756914
XF00518	gs://lims-analysis/rna_seq/SAMPLE-00029/2026-03-29/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00029	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:54.982808	2026-04-07 14:00:54.982808
XF00523	gs://lims-analysis/rna_seq/SAMPLE-00032/2026-04-01/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00032	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:56.282009	2026-04-07 14:00:56.282009
XF00528	gs://lims-analysis/chip_seq/SAMPLE-00034/2026-04-03/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00034	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:57.039513	2026-04-07 14:00:57.039513
XF00533	gs://lims-analysis/rna_seq/SAMPLE-00037/2026-04-06/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00037	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:57.901935	2026-04-07 14:00:57.901935
XF00538	gs://lims-analysis/rna_seq/SAMPLE-00039/2026-04-08/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00039	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:59.783139	2026-04-07 14:00:59.783139
XF00543	gs://lims-analysis/rna_seq/SAMPLE-00042/2026-04-11/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00042	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:01.879109	2026-04-07 14:01:01.879109
XF00548	gs://lims-analysis/chip_seq/SAMPLE-00044/2026-04-13/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00044	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:04.03353	2026-04-07 14:01:04.03353
XF00553	gs://lims-analysis/rna_seq/SAMPLE-00047/2026-04-16/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00047	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:04.817702	2026-04-07 14:01:04.817702
XF00558	gs://lims-analysis/rna_seq/SAMPLE-00049/2026-04-18/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00049	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:05.644765	2026-04-07 14:01:05.644765
XF00463	gs://lims-analysis/rna_seq/SAMPLE-00002/2026-03-02/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00002	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:40.932327	2026-04-07 14:00:40.932327
XF00466	gs://lims-analysis/chip_seq/SAMPLE-00003/2026-03-03/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00003	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:42.336715	2026-04-07 14:00:42.336715
XF00469	gs://lims-analysis/atac_seq/SAMPLE-00005/2026-03-05/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00005	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:43.102658	2026-04-07 14:00:43.102658
XF00472	gs://lims-analysis/atac_seq/SAMPLE-00006/2026-03-06/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00006	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:43.62947	2026-04-07 14:00:43.62947
XF00475	gs://lims-analysis/chip_seq/SAMPLE-00008/2026-03-08/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00008	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:44.186088	2026-04-07 14:00:44.186088
XF00478	gs://lims-analysis/rna_seq/SAMPLE-00009/2026-03-09/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00009	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:44.577421	2026-04-07 14:00:44.577421
XF00121	gs://lims-raw/FC-00001/lane1/SAMPLE-00001_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00001	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:43.736669	2026-04-07 13:06:43.736669
XF00122	gs://lims-raw/FC-00001/lane1/SAMPLE-00001_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00001	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:43.795234	2026-04-07 13:06:43.795234
XF00123	gs://lims-raw/FC-00002/lane1/SAMPLE-00002_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00002	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:43.857303	2026-04-07 13:06:43.857303
XF00124	gs://lims-raw/FC-00002/lane1/SAMPLE-00002_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00002	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:43.915738	2026-04-07 13:06:43.915738
XF00125	gs://lims-raw/FC-00003/lane2/SAMPLE-00003_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00003	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:43.971573	2026-04-07 13:06:43.971573
XF00126	gs://lims-raw/FC-00003/lane2/SAMPLE-00003_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00003	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.026645	2026-04-07 13:06:44.026645
XF00127	gs://lims-raw/FC-00004/lane2/SAMPLE-00004_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00004	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.089059	2026-04-07 13:06:44.089059
XF00128	gs://lims-raw/FC-00004/lane2/SAMPLE-00004_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00004	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.166975	2026-04-07 13:06:44.166975
XF00129	gs://lims-raw/FC-00005/lane3/SAMPLE-00005_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00005	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.235805	2026-04-07 13:06:44.235805
XF00130	gs://lims-raw/FC-00005/lane3/SAMPLE-00005_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00005	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.279097	2026-04-07 13:06:44.279097
XF00131	gs://lims-raw/FC-00001/lane2/SAMPLE-00006_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00006	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.346683	2026-04-07 13:06:44.346683
XF00132	gs://lims-raw/FC-00001/lane2/SAMPLE-00006_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00006	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.416299	2026-04-07 13:06:44.416299
XF00133	gs://lims-raw/FC-00002/lane2/SAMPLE-00007_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00007	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.483006	2026-04-07 13:06:44.483006
XF00134	gs://lims-raw/FC-00002/lane2/SAMPLE-00007_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00007	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.548463	2026-04-07 13:06:44.548463
XF00135	gs://lims-raw/FC-00003/lane3/SAMPLE-00008_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00008	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.596159	2026-04-07 13:06:44.596159
XF00136	gs://lims-raw/FC-00003/lane3/SAMPLE-00008_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00008	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.657402	2026-04-07 13:06:44.657402
XF00137	gs://lims-raw/FC-00004/lane3/SAMPLE-00009_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00009	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.7187	2026-04-07 13:06:44.7187
XF00138	gs://lims-raw/FC-00004/lane3/SAMPLE-00009_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00009	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.773696	2026-04-07 13:06:44.773696
XF00139	gs://lims-raw/FC-00005/lane4/SAMPLE-00010_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00010	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.845582	2026-04-07 13:06:44.845582
XF00140	gs://lims-raw/FC-00005/lane4/SAMPLE-00010_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00010	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:44.906507	2026-04-07 13:06:44.906507
XF00141	gs://lims-raw/FC-00001/lane3/SAMPLE-00011_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00011	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:44.986671	2026-04-07 13:06:44.986671
XF00142	gs://lims-raw/FC-00001/lane3/SAMPLE-00011_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00011	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.049827	2026-04-07 13:06:45.049827
XF00143	gs://lims-raw/FC-00002/lane3/SAMPLE-00012_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00012	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.103687	2026-04-07 13:06:45.103687
XF00144	gs://lims-raw/FC-00002/lane3/SAMPLE-00012_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00012	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.163899	2026-04-07 13:06:45.163899
XF00145	gs://lims-raw/FC-00003/lane4/SAMPLE-00013_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00013	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.212668	2026-04-07 13:06:45.212668
XF00146	gs://lims-raw/FC-00003/lane4/SAMPLE-00013_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00013	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.264777	2026-04-07 13:06:45.264777
XF00147	gs://lims-raw/FC-00004/lane4/SAMPLE-00014_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00014	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.315583	2026-04-07 13:06:45.315583
XF00148	gs://lims-raw/FC-00004/lane4/SAMPLE-00014_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00014	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.376104	2026-04-07 13:06:45.376104
XF00149	gs://lims-raw/FC-00005/lane1/SAMPLE-00015_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00015	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.423923	2026-04-07 13:06:45.423923
XF00150	gs://lims-raw/FC-00005/lane1/SAMPLE-00015_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00015	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.472699	2026-04-07 13:06:45.472699
XF00151	gs://lims-raw/FC-00001/lane4/SAMPLE-00016_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00016	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.517611	2026-04-07 13:06:45.517611
XF00152	gs://lims-raw/FC-00001/lane4/SAMPLE-00016_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00016	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.566033	2026-04-07 13:06:45.566033
XF00153	gs://lims-raw/FC-00002/lane4/SAMPLE-00017_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00017	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.610607	2026-04-07 13:06:45.610607
XF00154	gs://lims-raw/FC-00002/lane4/SAMPLE-00017_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00017	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.65765	2026-04-07 13:06:45.65765
XF00155	gs://lims-raw/FC-00003/lane1/SAMPLE-00018_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00018	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.72523	2026-04-07 13:06:45.72523
XF00156	gs://lims-raw/FC-00003/lane1/SAMPLE-00018_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00018	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.787311	2026-04-07 13:06:45.787311
XF00157	gs://lims-raw/FC-00004/lane1/SAMPLE-00019_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00019	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.850491	2026-04-07 13:06:45.850491
XF00158	gs://lims-raw/FC-00004/lane1/SAMPLE-00019_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00019	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:45.919342	2026-04-07 13:06:45.919342
XF00159	gs://lims-raw/FC-00005/lane2/SAMPLE-00020_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00020	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:45.975758	2026-04-07 13:06:45.975758
XF00160	gs://lims-raw/FC-00005/lane2/SAMPLE-00020_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00020	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.02299	2026-04-07 13:06:46.02299
XF00161	gs://lims-raw/FC-00001/lane1/SAMPLE-00021_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00021	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.083513	2026-04-07 13:06:46.083513
XF00162	gs://lims-raw/FC-00001/lane1/SAMPLE-00021_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00021	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.131865	2026-04-07 13:06:46.131865
XF00163	gs://lims-raw/FC-00002/lane1/SAMPLE-00022_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00022	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.181905	2026-04-07 13:06:46.181905
XF00164	gs://lims-raw/FC-00002/lane1/SAMPLE-00022_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00022	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.256495	2026-04-07 13:06:46.256495
XF00165	gs://lims-raw/FC-00003/lane2/SAMPLE-00023_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00023	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.33916	2026-04-07 13:06:46.33916
XF00166	gs://lims-raw/FC-00003/lane2/SAMPLE-00023_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00023	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.388937	2026-04-07 13:06:46.388937
XF00167	gs://lims-raw/FC-00004/lane2/SAMPLE-00024_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00024	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.442518	2026-04-07 13:06:46.442518
XF00168	gs://lims-raw/FC-00004/lane2/SAMPLE-00024_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00024	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.492517	2026-04-07 13:06:46.492517
XF00169	gs://lims-raw/FC-00005/lane3/SAMPLE-00025_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00025	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.533872	2026-04-07 13:06:46.533872
XF00170	gs://lims-raw/FC-00005/lane3/SAMPLE-00025_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00025	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.580618	2026-04-07 13:06:46.580618
XF00171	gs://lims-raw/FC-00001/lane2/SAMPLE-00026_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00026	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.630546	2026-04-07 13:06:46.630546
XF00172	gs://lims-raw/FC-00001/lane2/SAMPLE-00026_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00026	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.691317	2026-04-07 13:06:46.691317
XF00173	gs://lims-raw/FC-00002/lane2/SAMPLE-00027_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00027	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.748034	2026-04-07 13:06:46.748034
XF00174	gs://lims-raw/FC-00002/lane2/SAMPLE-00027_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00027	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.798814	2026-04-07 13:06:46.798814
XF00175	gs://lims-raw/FC-00003/lane3/SAMPLE-00028_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00028	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.858732	2026-04-07 13:06:46.858732
XF00176	gs://lims-raw/FC-00003/lane3/SAMPLE-00028_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00028	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:46.901301	2026-04-07 13:06:46.901301
XF00177	gs://lims-raw/FC-00004/lane3/SAMPLE-00029_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00029	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:46.957097	2026-04-07 13:06:46.957097
XF00178	gs://lims-raw/FC-00004/lane3/SAMPLE-00029_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00029	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.012488	2026-04-07 13:06:47.012488
XF00179	gs://lims-raw/FC-00005/lane4/SAMPLE-00030_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00030	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.068885	2026-04-07 13:06:47.068885
XF00180	gs://lims-raw/FC-00005/lane4/SAMPLE-00030_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00030	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.128508	2026-04-07 13:06:47.128508
XF00181	gs://lims-raw/FC-00001/lane3/SAMPLE-00031_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00031	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.19461	2026-04-07 13:06:47.19461
XF00182	gs://lims-raw/FC-00001/lane3/SAMPLE-00031_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00031	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.242885	2026-04-07 13:06:47.242885
XF00183	gs://lims-raw/FC-00002/lane3/SAMPLE-00032_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00032	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.298128	2026-04-07 13:06:47.298128
XF00184	gs://lims-raw/FC-00002/lane3/SAMPLE-00032_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00032	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.344228	2026-04-07 13:06:47.344228
XF00185	gs://lims-raw/FC-00003/lane4/SAMPLE-00033_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00033	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.396001	2026-04-07 13:06:47.396001
XF00186	gs://lims-raw/FC-00003/lane4/SAMPLE-00033_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00033	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.448445	2026-04-07 13:06:47.448445
XF00187	gs://lims-raw/FC-00004/lane4/SAMPLE-00034_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00034	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.499895	2026-04-07 13:06:47.499895
XF00188	gs://lims-raw/FC-00004/lane4/SAMPLE-00034_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00034	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.560425	2026-04-07 13:06:47.560425
XF00189	gs://lims-raw/FC-00005/lane1/SAMPLE-00035_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00035	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.624227	2026-04-07 13:06:47.624227
XF00190	gs://lims-raw/FC-00005/lane1/SAMPLE-00035_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00035	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.686564	2026-04-07 13:06:47.686564
XF00191	gs://lims-raw/FC-00001/lane4/SAMPLE-00036_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00036	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.734204	2026-04-07 13:06:47.734204
XF00192	gs://lims-raw/FC-00001/lane4/SAMPLE-00036_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00036	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.785121	2026-04-07 13:06:47.785121
XF00193	gs://lims-raw/FC-00002/lane4/SAMPLE-00037_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00037	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.833796	2026-04-07 13:06:47.833796
XF00194	gs://lims-raw/FC-00002/lane4/SAMPLE-00037_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00037	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.890866	2026-04-07 13:06:47.890866
XF00195	gs://lims-raw/FC-00003/lane1/SAMPLE-00038_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00038	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:47.936893	2026-04-07 13:06:47.936893
XF00196	gs://lims-raw/FC-00003/lane1/SAMPLE-00038_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00038	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:47.982959	2026-04-07 13:06:47.982959
XF00197	gs://lims-raw/FC-00004/lane1/SAMPLE-00039_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00039	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.057565	2026-04-07 13:06:48.057565
XF00198	gs://lims-raw/FC-00004/lane1/SAMPLE-00039_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00039	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.110822	2026-04-07 13:06:48.110822
XF00199	gs://lims-raw/FC-00005/lane2/SAMPLE-00040_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00040	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.157781	2026-04-07 13:06:48.157781
XF00200	gs://lims-raw/FC-00005/lane2/SAMPLE-00040_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00040	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.205735	2026-04-07 13:06:48.205735
XF00201	gs://lims-raw/FC-00001/lane1/SAMPLE-00041_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00041	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.247229	2026-04-07 13:06:48.247229
XF00202	gs://lims-raw/FC-00001/lane1/SAMPLE-00041_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00041	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.299922	2026-04-07 13:06:48.299922
XF00203	gs://lims-raw/FC-00002/lane1/SAMPLE-00042_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00042	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.357027	2026-04-07 13:06:48.357027
XF00204	gs://lims-raw/FC-00002/lane1/SAMPLE-00042_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00042	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.416724	2026-04-07 13:06:48.416724
XF00205	gs://lims-raw/FC-00003/lane2/SAMPLE-00043_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00043	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.470616	2026-04-07 13:06:48.470616
XF00206	gs://lims-raw/FC-00003/lane2/SAMPLE-00043_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00043	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.540259	2026-04-07 13:06:48.540259
XF00207	gs://lims-raw/FC-00004/lane2/SAMPLE-00044_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00044	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.596525	2026-04-07 13:06:48.596525
XF00208	gs://lims-raw/FC-00004/lane2/SAMPLE-00044_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00044	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.644535	2026-04-07 13:06:48.644535
XF00209	gs://lims-raw/FC-00005/lane3/SAMPLE-00045_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00045	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.699173	2026-04-07 13:06:48.699173
XF00210	gs://lims-raw/FC-00005/lane3/SAMPLE-00045_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00045	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.75176	2026-04-07 13:06:48.75176
XF00211	gs://lims-raw/FC-00001/lane2/SAMPLE-00046_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00046	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.794795	2026-04-07 13:06:48.794795
XF00212	gs://lims-raw/FC-00001/lane2/SAMPLE-00046_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00046	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.836479	2026-04-07 13:06:48.836479
XF00213	gs://lims-raw/FC-00002/lane2/SAMPLE-00047_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00047	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:48.90285	2026-04-07 13:06:48.90285
XF00214	gs://lims-raw/FC-00002/lane2/SAMPLE-00047_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00047	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:48.997732	2026-04-07 13:06:48.997732
XF00215	gs://lims-raw/FC-00003/lane3/SAMPLE-00048_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00048	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:49.06768	2026-04-07 13:06:49.06768
XF00216	gs://lims-raw/FC-00003/lane3/SAMPLE-00048_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00048	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:49.135043	2026-04-07 13:06:49.135043
XF00217	gs://lims-raw/FC-00004/lane3/SAMPLE-00049_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00049	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:49.197876	2026-04-07 13:06:49.197876
XF00218	gs://lims-raw/FC-00004/lane3/SAMPLE-00049_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00049	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:49.258845	2026-04-07 13:06:49.258845
XF00219	gs://lims-raw/FC-00005/lane4/SAMPLE-00050_R1.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00050	\N	{"extra_metadata": "{\\"read\\": \\"R1\\"}"}	2026-04-07 13:06:49.323	2026-04-07 13:06:49.323
XF00220	gs://lims-raw/FC-00005/lane4/SAMPLE-00050_R2.fastq.gz	lims-raw	\N	fastq	fastq.gz	\N	\N	XER00050	\N	{"extra_metadata": "{\\"read\\": \\"R2\\"}"}	2026-04-07 13:06:49.395261	2026-04-07 13:06:49.395261
XF00221	gs://lims-analysis/rna_seq/SAMPLE-00001/2026-03-01/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00001	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:49.468522	2026-04-07 13:06:49.468522
XF00222	gs://lims-analysis/atac_seq/SAMPLE-00005/2026-03-05/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00005	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:49.906833	2026-04-07 13:06:49.906833
XF00223	gs://lims-analysis/atac_seq/SAMPLE-00006/2026-03-06/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00006	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:49.967625	2026-04-07 13:06:49.967625
XF00224	gs://lims-analysis/atac_seq/SAMPLE-00010/2026-03-10/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00010	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:50.559018	2026-04-07 13:06:50.559018
XF00225	gs://lims-analysis/rna_seq/SAMPLE-00011/2026-03-11/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00011	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:50.602271	2026-04-07 13:06:50.602271
XF00226	gs://lims-analysis/atac_seq/SAMPLE-00015/2026-03-15/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00015	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:51.146404	2026-04-07 13:06:51.146404
XF00227	gs://lims-analysis/atac_seq/SAMPLE-00016/2026-03-16/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00016	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:51.213617	2026-04-07 13:06:51.213617
XF00228	gs://lims-analysis/atac_seq/SAMPLE-00020/2026-03-20/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00020	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:51.687612	2026-04-07 13:06:51.687612
XF00229	gs://lims-analysis/rna_seq/SAMPLE-00021/2026-03-21/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00021	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:51.741798	2026-04-07 13:06:51.741798
XF00230	gs://lims-analysis/atac_seq/SAMPLE-00025/2026-03-25/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00025	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:52.265787	2026-04-07 13:06:52.265787
XF00231	gs://lims-analysis/atac_seq/SAMPLE-00026/2026-03-26/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00026	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:52.338918	2026-04-07 13:06:52.338918
XF00235	gs://lims-analysis/atac_seq/SAMPLE-00036/2026-04-05/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00036	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:53.582598	2026-04-07 13:06:53.582598
XF00239	gs://lims-analysis/atac_seq/SAMPLE-00046/2026-04-15/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00046	\N	{"extra_metadata": "{}"}	2026-04-07 13:06:54.731569	2026-04-07 13:06:54.731569
XF00514	gs://lims-analysis/rna_seq/SAMPLE-00027/2026-03-27/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00027	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:54.392205	2026-04-07 14:00:54.392205
XF00519	gs://lims-analysis/atac_seq/SAMPLE-00030/2026-03-30/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00030	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:55.590408	2026-04-07 14:00:55.590408
XF00524	gs://lims-analysis/rna_seq/SAMPLE-00032/2026-04-01/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00032	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:56.463509	2026-04-07 14:00:56.463509
XF00529	gs://lims-analysis/atac_seq/SAMPLE-00035/2026-04-04/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00035	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:57.262362	2026-04-07 14:00:57.262362
XF00534	gs://lims-analysis/rna_seq/SAMPLE-00037/2026-04-06/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00037	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:58.15365	2026-04-07 14:00:58.15365
XF00539	gs://lims-analysis/atac_seq/SAMPLE-00040/2026-04-09/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00040	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:00.571365	2026-04-07 14:01:00.571365
XF00544	gs://lims-analysis/rna_seq/SAMPLE-00042/2026-04-11/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00042	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:02.098885	2026-04-07 14:01:02.098885
XF00549	gs://lims-analysis/atac_seq/SAMPLE-00045/2026-04-14/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00045	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:04.174874	2026-04-07 14:01:04.174874
XF00554	gs://lims-analysis/rna_seq/SAMPLE-00047/2026-04-16/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00047	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:04.961359	2026-04-07 14:01:04.961359
XF00559	gs://lims-analysis/atac_seq/SAMPLE-00050/2026-04-19/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00050	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:05.783997	2026-04-07 14:01:05.783997
XF00498	gs://lims-analysis/rna_seq/SAMPLE-00019/2026-03-19/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00019	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:50.78931	2026-04-07 14:00:50.78931
XF00499	gs://lims-analysis/atac_seq/SAMPLE-00020/2026-03-20/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00020	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:50.92717	2026-04-07 14:00:50.92717
XF00515	gs://lims-analysis/chip_seq/SAMPLE-00028/2026-03-28/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00028	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:54.53604	2026-04-07 14:00:54.53604
XF00502	gs://lims-analysis/rna_seq/SAMPLE-00021/2026-03-21/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00021	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:51.542273	2026-04-07 14:00:51.542273
XF00503	gs://lims-analysis/rna_seq/SAMPLE-00022/2026-03-22/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00022	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:51.695035	2026-04-07 14:00:51.695035
XF00504	gs://lims-analysis/rna_seq/SAMPLE-00022/2026-03-22/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00022	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:51.823098	2026-04-07 14:00:51.823098
XF00505	gs://lims-analysis/chip_seq/SAMPLE-00023/2026-03-23/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00023	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:52.558102	2026-04-07 14:00:52.558102
XF00506	gs://lims-analysis/chip_seq/SAMPLE-00023/2026-03-23/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00023	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:52.673414	2026-04-07 14:00:52.673414
XF00507	gs://lims-analysis/chip_seq/SAMPLE-00024/2026-03-24/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00024	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:52.797386	2026-04-07 14:00:52.797386
XF00508	gs://lims-analysis/chip_seq/SAMPLE-00024/2026-03-24/qc_html.html	lims-analysis	\N	qc_html	html	\N	\N	XER00024	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:52.926055	2026-04-07 14:00:52.926055
XF00509	gs://lims-analysis/atac_seq/SAMPLE-00025/2026-03-25/counts.tsv	lims-analysis	\N	counts	tsv	\N	\N	XER00025	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:53.11346	2026-04-07 14:00:53.11346
XF00525	gs://lims-analysis/chip_seq/SAMPLE-00033/2026-04-02/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00033	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:56.591972	2026-04-07 14:00:56.591972
XF00535	gs://lims-analysis/chip_seq/SAMPLE-00038/2026-04-07/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00038	\N	{"extra_metadata": "{}"}	2026-04-07 14:00:58.274102	2026-04-07 14:00:58.274102
XF00545	gs://lims-analysis/chip_seq/SAMPLE-00043/2026-04-12/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00043	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:03.068611	2026-04-07 14:01:03.068611
XF00555	gs://lims-analysis/chip_seq/SAMPLE-00048/2026-04-17/vcf.vcf.gz	lims-analysis	\N	vcf	vcf.gz	\N	\N	XER00048	\N	{"extra_metadata": "{}"}	2026-04-07 14:01:05.097474	2026-04-07 14:01:05.097474
\.


--
-- TOC entry 3929 (class 0 OID 20907)
-- Dependencies: 227
-- Data for Name: id_concordance; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.id_concordance (id, entity_type, internal_id, source_system, external_id, created_at) FROM stdin;
\.


--
-- TOC entry 3925 (class 0 OID 20881)
-- Dependencies: 223
-- Data for Name: metadata_registry; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.metadata_registry (id, entity_type, field_name, data_type, allowed_values, description, version, created_at) FROM stdin;
\.


--
-- TOC entry 3927 (class 0 OID 20894)
-- Dependencies: 225
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: public; Owner: chene
--

COPY public.schema_migrations (id, migration_name, applied_at) FROM stdin;
\.


--
-- TOC entry 3936 (class 0 OID 0)
-- Dependencies: 213
-- Name: experiment_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.experiment_seq', 50, true);


--
-- TOC entry 3937 (class 0 OID 0)
-- Dependencies: 216
-- Name: files_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.files_seq', 760, true);


--
-- TOC entry 3938 (class 0 OID 0)
-- Dependencies: 226
-- Name: id_concordance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.id_concordance_id_seq', 1, false);


--
-- TOC entry 3939 (class 0 OID 0)
-- Dependencies: 222
-- Name: metadata_registry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.metadata_registry_id_seq', 1, false);


--
-- TOC entry 3940 (class 0 OID 0)
-- Dependencies: 211
-- Name: project_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.project_seq', 42, true);


--
-- TOC entry 3941 (class 0 OID 0)
-- Dependencies: 215
-- Name: run_exp_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.run_exp_seq', 50, true);


--
-- TOC entry 3942 (class 0 OID 0)
-- Dependencies: 214
-- Name: run_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.run_seq', 5, true);


--
-- TOC entry 3943 (class 0 OID 0)
-- Dependencies: 212
-- Name: sample_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.sample_seq', 50, true);


--
-- TOC entry 3944 (class 0 OID 0)
-- Dependencies: 224
-- Name: schema_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chene
--

SELECT pg_catalog.setval('public.schema_migrations_id_seq', 1, false);


-- Completed on 2026-06-09 12:37:46 EDT

--
-- PostgreSQL database dump complete
--

\unrestrict yuh7edZbC5MVOCV3cHxvheswluHMiQEAjKshV6qHohjXl7yRyYCohQxbrXehS4d

