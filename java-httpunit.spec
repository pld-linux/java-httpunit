# TODO
# - disable tests that use network and $DISPLAY
Summary:	Automated web site testing toolkit
Summary(pl.UTF-8):	Zestaw narzędzi do automatycznego testowania serwisów WWW
Name:		httpunit
Version:	1.6
Release:	1
Epoch:		0
License:	MIT
Group:		Development
Source0:	http://dl.sourceforge.net/httpunit/%{name}-%{version}.zip
# Source0-md5:	e94b53b9f4d7bdb706e4baac95b6e424
Patch0:		%{name}.build.patch
Patch1:		%{name}-JavaScript-NotAFunctionException.patch
Patch2:		%{name}-servlettest.patch
Patch3:		%{name}-java15.patch
URL:		http://httpunit.sourceforge.net/
# As of 1.5, requires either nekohtml or jtidy, and prefers nekohtml.
BuildRequires:	ant
BuildRequires:	jaf >= 0:1.0.1
BuildRequires:	jakarta-servletapi
BuildRequires:	javamail >= 0:1.2
BuildRequires:	jtidy
BuildRequires:	junit < 4.0
BuildRequires:	junit >= 3.8
# nekohtml broken
#BuildRequires:	nekohtml
BuildRequires:	rhino
BuildRequires:	unzip
Requires:	jaxp_parser_impl
Requires:	jtidy
Requires:	junit >= 0:3.8
#Requires:	nekohtml
Requires:	rhino
Requires:	servlet23
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

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package manual
Summary:	Manual for %{name}
Summary(pl.UTF-8):	Podręcznik dla pakietu %{name}
Group:		Development

%description manual
Documentation for %{name}.

%description manual -l pl.UTF-8
Podręcznik dla pakietu %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{name}
Group:		Development
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{name}.

%prep
%setup -q
%patch0 -p0
%patch1
%patch2
%patch3
%{__unzip} -qd META-INF lib/httpunit.jar '*.dtd' # 1.6 dist zip is borked
# remove all binary libs and javadocs
find -name '*.jar' | xargs rm -v
rm -rf doc/api
ln -s \
  %{_javadir}/junit.jar \
  %{_javadir}/jtidy.jar \
  %{_javadir}/nekohtml.jar \
  %{_javadir}/servletapi4.jar \
  %{_javadir}/js.jar \
  %{_javadir}/xerces-j2.jar \
  jars

%build
export CLASSPATH=$(build-classpath jaf javamail junit)
%ant -Dbuild.compiler=modern -Dbuild.sysclasspath=last \
  jar testjar examplesjar javadocs test servlettest

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp -a lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# Avoid having api in manual
rm -rf manual
cp -a doc manual
rm -rf manual/api
# Fix link between manual and javadoc
ln -sf %{_javadocdir}/%{name}-%{version} manual/api

# Demo
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a lib/%{name}-test.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-test-%{version}.jar
cp -a lib/%{name}-examples.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-examples-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%doc manual/*

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}
