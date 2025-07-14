# TODO
# - does not build with new servletapi.
# NOTE:
# As of 1.5, requires either nekohtml or jtidy, and prefers nekohtml.
#
# Conditional build:
%bcond_with	jtidy		# jtidy vs nekohtml
%bcond_with	tests		# perform tests (seems to be broken)
%bcond_without	javadoc		# perform tests (seems to be broken)

#
%define		srcname		httpunit
Summary:	Automated web site testing toolkit
Summary(pl.UTF-8):	Zestaw narzędzi do automatycznego testowania serwisów WWW
Name:		java-httpunit
Version:	1.6
Release:	1
Epoch:		0
License:	MIT
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/httpunit/%{srcname}-%{version}.zip
# Source0-md5:	e94b53b9f4d7bdb706e4baac95b6e424
Patch0:		%{srcname}.build.patch
Patch1:		%{srcname}-JavaScript-NotAFunctionException.patch
Patch2:		%{srcname}-servlettest.patch
Patch3:		%{srcname}-java15.patch
URL:		http://httpunit.sourceforge.net/
# BuildRequires:	java(servlet) >= 2.3
BuildRequires:	ant
BuildRequires:	java(jaf) >= 1.0.1
BuildRequires:	java(javamail) >= 0:1.2
BuildRequires:	java-rhino >= 1.5R4.1
BuildRequires:	java-xerces >= 2.5
BuildRequires:	jdk
%{?with_jtidy:BuildRequires:	jtidy >= 1.0-0.20000804r7dev}
BuildRequires:	junit >= 3.8
%{!?with_jtidy:BuildRequires:	nekohtml >= 0.9.1}
BuildRequires:	unzip
# Requires:	java(servlet) >= 2.3
Requires:	java-junit >= 0:3.8
Requires:	java-rhino >= 1.5R4.1
Requires:	java-xerces >= 2.5
%{?with_jtidy:Requires:	jtidy >= 1.0-0.20000804r7dev}
%{!?with_jtidy:Requires:	nekohtml >= 0.9.1}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HttpUnit emulates the relevant portions of browser behavior, including
form submission, JavaScript, basic HTTP authentication, cookies and
automatic page redirection, and allows Java test code to examine
returned pages either as text, an XML DOM, or containers of forms,
tables, and links. A companion framework, ServletUnit is included in
the package.

%description -l pl.UTF-8
HttpUnit emuluje odpowiednie elementy zachowania przeglądarki włącznie
z wysyłaniem formularzy, JavaScriptem, podstawowym uwierzytelnieniem
HTTP, ciasteczkami i automatycznym przekierowywaniem stron oraz
pozwala testowemu kodowi w Javie sprawdzać zwracane strony jako tekst,
XML DOM lub kontenery formularzy, tabel i odnośników. W pakiecie
załączony jest także towarzyszący szkielet - ServletUnit.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package manual
Summary:	Manual for %{name}
Summary(pl.UTF-8):	Podręcznik dla pakietu %{name}
Group:		Documentation

%description manual
Documentation for %{name}.

%description manual -l pl.UTF-8
Podręcznik dla pakietu %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{name}
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{name}.

%prep
%setup -q -n %{srcname}-%{version}
%patch -P0 -p0
%patch -P1
%patch -P2
%patch -P3
%{__unzip} -qd META-INF lib/httpunit.jar '*.dtd' # 1.6 dist zip is borken

find -name '*.jar' | xargs rm -v
rm -rf doc/api

%build

ln -s $(find-jar junit) jars/junit.jar
#ln -s $(find-jar servlet) jars/servlet.jar
ln -s $(find-jar xerces) jars/xerces.jar
%{?with_jtidy:ln -s $(find-jar jtidy) jars/Tidy.jar}
%{!?with_jtidy:ln -s $(find-jar nekohtml) jars/nekohtml.jar}
ln -s $(find-jar js) jars/js.jar

%ant \
	jar \
	testjar \
	examplesjar \
	%{?with_javadoc:javadocs}

%if %{with tests}
%ant \
	test \
	servlettest
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp -a lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with javadoc}
# Javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# Avoid having api in manual
rm -rf manual
cp -a doc manual
rm -rf manual/api

# Demo
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_examplesdir}/%{name}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a lib/%{srcname}-test.jar \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/%{srcname}-test-%{version}.jar
cp -a lib/%{srcname}-examples.jar \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/%{srcname}-examples-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%if %{with javadoc}

%files manual
%defattr(644,root,root,755)
%doc manual/*

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
%{_examplesdir}/%{name}
