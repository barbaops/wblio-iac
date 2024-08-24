# EKS FULL

Repositório de IaC para subir todos os recursos de uso do EKS separados por tipo de ferramenta de IaC.

## Arquitetura base e exemplos

EM BREVE


## Modulo 1 - NETWORK

O primeiro modulo a ser criado é o de Network, nele iremos subir VPCs, Subnets e Gateways de disponibilidade


### VPC

Uma VPC proporciona um isolamento rigoroso da sua rede na AWS de outras redes. Este isolamento é alcançado através de uma fronteira virtual que controla o acesso e o tráfego entre as redes. Dessa forma, organizações podem executar suas aplicações em um ambiente de nuvem privado, gerenciando o acesso de maneira segura e eficaz.

Com as VPCs, você obtém controle granular sobre as dimensões e definições de sua rede. Isso inclui:

Seleção do Intervalo de Endereços IP: Você pode escolher o bloco de IPs que será utilizado pela sua VPC.
Criação de Sub-redes: Dividir sua VPC em sub-redes permite segmentar e controlar o acesso a diferentes partes da sua rede.
Configuração de Tabelas de Rotas e Gateways de Rede: Essas ferramentas permitem definir como o tráfego é direcionado e gerenciado dentro da sua VPC e para o exterior.
Grupos de Segurança: Atuam como firewalls virtuais para suas instâncias, controlando o tráfego de entrada e saída.
Listas de Controle de Acesso à Rede (NACLs): Fornecem um nível adicional de controle de tráfego para e entre suas sub-redes.

### SUBNET

Subnets, ou sub-redes, são divisões de uma rede maior. No contexto de uma Virtual Private Cloud (VPC) na AWS, subnets permitem que você segmente a VPC em redes menores, o que facilita a organização, o gerenciamento de tráfego e a aplicação de políticas de segurança de maneira mais granular.

Cada subnet pode ser configurada para hospedar uma parte diferente da infraestrutura, como aplicações front-end, back-end, ou bancos de dados, permitindo o isolamento entre esses componentes. Você pode criar essas sub-redes, que podem ser públicas (com acesso direto à Internet) ou privadas (sem acesso direto à Internet), para hospedar diferentes tipos de aplicações com base em requisitos de visibilidade e acesso

#### PUBLIC

Subnets públicas são aquelas configuradas para permitir acesso direto à Internet de forma bilateral, ou seja, os recursos pertencentes a ela podem acessar a internet tanto como podem ser acessados diretamente por meio dela. Elas são essenciais para hospedar recursos que precisam ser acessíveis externamente, como servidores web, proxies e gateways. Recursos nestas subnets são atribuídos a um Endereço IP público, permitindo-lhes comunicar-se com a Internet e serem acessados por usuários externos.

#### PRIVATE

Subnets privadas são utilizadas para recursos que não devem ser acessados diretamente da Internet. Essas subnets não possuem rotas para a Internet, garantindo que o acesso externo seja bloqueado. Recursos nessas áreas da rede podem se comunicar com a Internet ou outros serviços externos através de soluções como NAT Gateways localizados em subnets públicas, mas não recebem tráfego direto da Internet. Elas são utilizadas para hospedar recursos como aplicações backend, servidores de aplicação, microserviços internos, e tarefas de processamento de dados e batchs e etc.

Além das medidas de segurança padrão, o acesso a estas subnets geralmente é controlado por VPNs ou Direct Connect, garantindo que apenas tráfego autorizado possa acessar os recursos.

#### DATABASE

Especificamente projetadas para hospedar bancos de dados, estas subnets são um tipo de subnet privada com regras adicionais de segurança e acessibilidade. Colocar bancos de dados em subnets dedicadas ajuda a proteger os dados sensíveis e otimizar a segurança, restringindo o acesso apenas a recursos autorizados dentro da VPC.

Utilizadas para hospedar recursos como bancos de dados SQL e NoSQL, caches em memória, e armazenamentos de dados em repouso.

Seu acesso é restrito a partir de subnets específicas, geralmente subnets de aplicação, e proteção adicional contra ataques e acesso não autorizado.

### GATEWAY / CONECTIVIDADE

#### Internet Gateway (IGW)

Um IGW permite que suas instâncias na VPC acessem a Internet, funcionando como um ponto de acesso público para suas aplicações. Utilizado em subnets públicas para prover acesso bidirecional a internet.

#### NAT Gateway

O NAT Gateway possibilita que instâncias em subnets privadas acessem recursos na Internet, mantendo o tráfego de entrada bloqueado, o que aumenta a segurança. Normalmente são criados em subnets públicas e são acessados pelas aplicações privadas através de regras de tabelas de rotas.

#### VPC Endpoints

Os VPC Endpoints permitem conexões privadas entre sua VPC e serviços AWS, eliminando a necessidade de tráfego passar pela Internet pública.

Existem dois tipos de endpoints, o Gateway Endpoint (para serviços como S3 e DynamoDB) e o Interface Endpoint (para outros serviços AWS ou customizados).

