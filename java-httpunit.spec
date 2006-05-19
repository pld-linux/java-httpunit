Summary:	Automated web site testing toolkit
Summary(pl):	Zestaw narzêdzi do automatycznego testowania serwisów WWW
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
BuildRequires:	jaf >= 0:1.0.1
BuildRequires:	ant
BuildRequires:	jakarta-servletapi
BuildRequires:	javamail >= 0:1.2
BuildRequires:	jtidy
BuildRequires:	junit >= 0:3.8
# nekohtml broken
#BuildRequires:	nekohtml
BuildRequires:	rhino
BuildRequires:	unzip
Requires:	jaxp_parser_impl
Requires:	junit >= 0:3.8
# As of 1.5, requires either nekohtml or jtidy, and prefers nekohtml.
Requires:	nekohtml
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

%description -l pl
HttpUnit emuluje odpowiednie elementy zachowania przegl±darki w³±cznie
z wysy³aniem formularzy, JavaScriptem, podstawowym uwierzytelnieniem
HTTP, ciasteczkami i automatycznym przekierowywaniem stron oraz
pozwala testowemu kodowi w Javie sprawdzaæ zwracane strony jako tekst,
XML DOM lub kontenery formularzy, tabel i odno¶ników. W pakiecie
za³±czony jest tak¿e towarzysz±cy szkielet - ServletUnit.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl
Dokumentacja javadoc dla pakietu %{name}.

%package manual
Summary:	Manual for %{name}
Summary(pl):	Podrêcznik dla pakietu %{name}
Group:		Development

%description manual
Documentation for %{name}.

%description manual -l pl
Podrêcznik dla pakietu %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl):	Pliki demonstracyjne dla pakietu %{name}
Group:		Development
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl
Pliki demonstracyjne i przyk³ady dla pakietu %{name}.

%prep
%setup -q
%patch0 -p0
%patch1
%patch2
%patch3
%{__unzip} -qd META-INF lib/httpunit.jar "*.dtd" # 1.6 dist zip is borked
# remove all binary libs and javadocs
find . -name "*.jar" -exec rm -f {} \;
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
export CLASSPATH=$(build-classpath jaf javamail)
ant -Dbuild.compiler=modern -Dbuild.sysclasspath=last \
  jar testjar examplesjar javadocs test servlettest

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp -p lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

# Jar versioning
cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}.jar; do
	ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
cd -

# Javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# Avoid having api in manual
rm -rf doc/api

# Fix link between manual and javadoc
ln -sf %{_javadocdir}/%{name}-%{version} doc/api

# Demo
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p lib/%{name}-test.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-test-%{version}.jar
cp -p lib/%{name}-examples.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-examples-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%{_javadir}/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}

%files manual
%defattr(644,root,root,755)
%doc doc/*

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}
